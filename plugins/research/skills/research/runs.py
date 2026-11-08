r"""Read my Weights & Biases runs: a table of the runs of a project, or the curves and diagnostics of one run.

Run it with the Python of the project environment, where `wandb login` was done: the key is never read nor printed.
  python runs.py sail-nyu/heimdall-training-encoders                   # every run: state, updates, losses, verdict
  python runs.py sail-nyu/heimdall-training-encoders --last 5          # the 5 most recent runs only
  python runs.py sail-nyu/heimdall-training-encoders --run <name>      # one run: its curves (20 points) and verdict
  python runs.py <entity/project> --keys "Training/Loss" "Validation/Loss" --points 30
Read only: nothing is written to WandB. If the API fails, the error is printed and nothing else is tried.
"""
import argparse
import math
import sys

TRAIN, VAL, GRAD = 'Training/Loss', 'Validation/Loss', 'Informations/Gradient Norm'
STEP = 'Informations/Steps Update'
SAMPLES = 1000  # points read per run (WandB samples the history)


def finite(values):
    return [v for v in values if isinstance(v, (int, float)) and math.isfinite(v)]


def series(history, key):
    """(step, value) of a logged key, in order, non-finite values kept as None."""
    out = []
    for row in history:
        if key in row and row[key] is not None:
            step = row.get(STEP, row.get('_step', len(out)))
            v = row[key]
            out.append((step, v if isinstance(v, (int, float)) and math.isfinite(v) else None))
    return out


def verdict(history):
    """One word on a run: diverged, overfitting, spikes or ok, with the number that says it."""
    train, val, grad = series(history, TRAIN), series(history, VAL), series(history, GRAD)
    if any(v is None for _, v in train + val):
        return 'diverged (non-finite loss)'
    for name, s in (('validation', val), ('training', train)):
        values = [v for _, v in s]
        if len(values) >= 5 and values[-1] > 3 * min(values):
            return f'diverged ({name} loss {values[-1]:.3g}, minimum {min(values):.3g})'
    if len(val) >= 5 and len(train) >= 5:
        values = [v for _, v in val]
        k = values.index(min(values))
        if k < 0.7 * len(values) and values[-1] > 1.2 * values[k]:
            t = [v for _, v in train]
            if t[-1] < t[min(k * len(t) // len(values), len(t) - 1)]:
                return f'overfitting (validation {values[k]:.3g} at step {val[k][0]}, now {values[-1]:.3g})'
    g = finite(v for _, v in grad)
    if len(g) >= 10:
        median = sorted(g)[len(g) // 2]
        spikes = sum(1 for v in g if v > 10 * median)
        if spikes:
            return f'spikes ({spikes} gradient norms above 10 times the median {median:.3g})'
    return 'ok'


def last(history, key):
    values = finite(v for _, v in series(history, key))
    return values[-1] if values else None


def fmt(v, width=10):
    return (f'{v:.4g}' if isinstance(v, (int, float)) else '-').rjust(width)


def table(runs, keys):
    head = f"{'run':<42} {'state':<9} {'updates':>8} " + ' '.join(k.split('/')[-1][:10].rjust(10) for k in keys)
    print(head + '  verdict')
    print('-' * (len(head) + 30))
    for run in runs:
        history = run.history(samples=SAMPLES, keys=keys + [STEP, GRAD], pandas=False)
        steps = finite(v for _, v in series(history, STEP))
        print(f"{run.name[:42]:<42} {run.state:<9} {int(steps[-1]) if steps else '-':>8} "
              + ' '.join(fmt(last(history, k)) for k in keys) + f'  {verdict(history)}')


def curves(run, keys, points):
    history = run.history(samples=SAMPLES, keys=keys + [STEP, GRAD], pandas=False)
    print(f'{run.name}: {run.state}, {verdict(history)}')
    print(f"{'step':>8} " + ' '.join(k.split('/')[-1][:12].rjust(12) for k in keys))
    rows = [row for row in history if any(k in row for k in keys)]
    stride = max(1, len(rows) // points)
    for row in rows[::stride] + ([rows[-1]] if rows and (len(rows) - 1) % stride else []):
        step = row.get(STEP, row.get('_step', '-'))
        print(f"{int(step) if isinstance(step, (int, float)) else step:>8} "
              + ' '.join(fmt(row.get(k), 12) for k in keys))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('project', help='entity/project, e.g. sail-nyu/heimdall-training-encoders')
    ap.add_argument('--run', help='name of one run: its curves and diagnostics')
    ap.add_argument('--last', type=int, help='only the N most recent runs')
    ap.add_argument('--keys', nargs='+', default=[TRAIN, VAL], help='logged metrics to show')
    ap.add_argument('--points', type=int, default=20, help='points per curve with --run')
    a = ap.parse_args()
    try:
        import wandb
        api = wandb.Api()
        runs = list(api.runs(a.project, order='-created_at'))
    except Exception as error:  # noqa: BLE001
        sys.exit(f'wandb.Api() failed: {type(error).__name__}: {error}. Stop and tell Victor; never ask for, '
                 'print or set the key.')
    if a.run:
        matches = [r for r in runs if r.name == a.run or r.id == a.run]
        if not matches:
            sys.exit(f'no run named {a.run!r} in {a.project}')
        curves(matches[0], a.keys, a.points)
    else:
        table(runs[:a.last] if a.last else runs, a.keys)
