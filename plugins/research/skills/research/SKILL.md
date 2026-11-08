---
name: research
description: "Use at the start of every session in one of my projects or libraries (Heimdall, Neptune, shaggy, albus), and whenever you need: what my projects study, who my supervisors are, which library to use before writing code (azula diffusion, zuko flows, shaggy training tools and autoencoders, albus metrics) and what it contains, the documentation links, or how to read my Weights & Biases runs (training curves, divergence, comparing runs)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Research: my projects, my supervisors and the
     ┌─┴───┴─┐       libraries to know and reuse before coding.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# RESEARCH

My projects, the people I work with, the libraries I build on and where my runs are logged. Check here before asking
me, and check the libraries before writing code: what you need may already exist.

**Last checked: 2026-11-04** (every link below was opened and verified on that day).

> **Keep this file up to date.** People, links and library APIs change. If the date above is more than one month
> old, before relying on this file:
> 1. launch **an agent with the model `haiku` and the effort `low`** to open every link below and list those that
>    fail or redirect, and **an agent with the model `sonnet`** to check the module tables of
>    `references/libraries.md` against the installed libraries;
> 2. propose the changes to me, then, after my approval, make them in a clone of VikVador/Claude through a pull
>    request, never in `~/.claude/plugins/`: that copy is overwritten at the next update.

| File                      | Use                                                        | When                                              |
| ------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| `references/libraries.md` | **Read**                                                   | before writing code a library could cover, or for its API |
| `runs.py`                 | **Run** `python <skill folder>/runs.py <entity/project>`   | to check or compare my WandB runs (§ 5)           |

Related: the `auto-update` skill updates `shaggy` and `albus` and asks to update § 3 when their API changes; the
`cluster-torch` and `cluster-lucia` skills for the clusters.

**Contents**

0. In short
1. Projects
2. People
3. Libraries
4. Documentation
5. Monitoring runs (WandB)
6. Open questions

---

## 0. IN SHORT

1. **Two projects**: Heimdall (global ocean, NYU, cluster Torch) and Neptune (Black Sea, ULiège, cluster Lucia) (§ 1).
2. **Three supervisors**: Gilles Louppe (SAIL) and Marilaure Grégoire (MAST) at ULiège, Laure Zanna (M²LInES) at NYU
   (§ 2).
3. **Check the libraries before coding**: diffusion → `azula`, flows → `zuko`, training tools, autoencoders and
   losses → `shaggy`, metrics → `albus`; read their module tables in `references/libraries.md` (§ 3).
4. **You can read my WandB runs yourself**: check the curves before asking me for screenshots (§ 5).
5. **Never touch the WandB key**: never ask for it, print it or set it; if `wandb.Api()` fails, tell me (§ 5).
6. **Runs are read only**: never delete, edit, tag or move a run (§ 5).
7. **Edits to this file**: ask me first, then a pull request in a clone of VikVador/Claude, never in
   `~/.claude/plugins/`.

---

## 1. PROJECTS

| Project  | Where        | Repository                                                           | Cluster   |
| -------- | ------------ | -------------------------------------------------------------------- | --------- |
| Heimdall | NYU, M²LInES | [github.com/VikVador/Heimdall](https://github.com/VikVador/Heimdall) | NYU Torch |
| Neptune  | ULiège       | [github.com/VikVador/Neptune](https://github.com/VikVador/Neptune)   | Lucia     |

### Heimdall

*"Exploring the Limits of Global Ocean State Estimation from Satellite Observations"*

| Item  | Details                                                                                                         |
| ----- | --------------------------------------------------------------------------------------------------------------- |
| Goal  | a latent generative model of the **global ocean state**, to find the limits of ocean predictability from space  |
| Data  | daily GLORYS reanalysis + daily surface observations (temperature, salinity, wind, chlorophyll; Copernicus L3)  |
| Model | one deterministic encoder per dataset, a stochastic transformer learning the joint dynamics in the latent space |
| Use   | long joint trajectories generated with score-based data assimilation                                            |
| Where | data 2000–2025 on the OSN pod of M²LInES, trainings on NYU Torch                                                |

### Neptune

*"Mastering the Black Sea Physics and Biogeochemistry with latent generative models"*

| Item                    | Details                                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------------------- |
| Goal                    | a generative **emulator of the Black Sea** forecasting the next daily state                     |
| Data                    | daily NEMO 4.2.0 simulation (576 × 256 grid, 48 levels, 1998–2023), ERA5 atmospheric forcing    |
| Splits                  | training 1998–2017, validation 2018–2020, test 2021–2022 (2023 set aside, being recomputed)     |
| State (surface)         | wind stress, sea surface height                                                                 |
| State (physics)         | currents, temperature, salinity                                                                 |
| State (biogeochemistry) | chlorophyll, oxygen, light, phosphate, silicate, nitrate                                        |
| Model                   | two approaches, **FGN** and **Latent** (below)                                                  |
| Where                   | data in `/gpfs/projects/acad/bsmfc/nemo4.2.0`, trainings on Lucia (jobs submitted with `dawgz`) |

**Good to know**

- **FGN** (`experiments/forecast-ambient-increments`): two `shaggy` ConvAEs (surface 2D, ocean 3D) and an `azula`
  DiT, trained end to end to output the daily increments. Training: ensemble members with a fair CRPS, conditioned on
  the date (and ERA5 for the surface), then fine-tuned on autoregressive rollouts.
- **Latent** (`experiments/forecast-latent-states`): staged, encoders trained with the GME loss, then a
  noise-conditioned processor of the latent state, then a decoder.

---

## 2. PEOPLE

| Person             | Role                                  | Lab                              | Links                                            |
| ------------------ | ------------------------------------- | -------------------------------- | ------------------------------------------------ |
| Gilles Louppe      | Supervisor, Professor at ULiège       | leads SAIL (Science with AI Lab) | [homepage][louppe], [SAIL][sail]                 |
| Marilaure Grégoire | Supervisor, Full Professor at ULiège  | leads MAST (ocean modelling)     | [MAST][mast], [FOCUS][focus]                     |
| Laure Zanna        | Supervisor at NYU (Courant Institute) | Lead PI of M²LInES               | [group][zanna], [M²LInES][m2lines], [team][team] |

[louppe]: https://glouppe.github.io/
[sail]: https://glouppe.github.io/sail/
[mast]: https://www.mast.uliege.be/cms/c_4938897/en/mast
[focus]: https://www.focus.uliege.be/cms/c_4262877/en/focus
[zanna]: https://zanna-researchteam.github.io/
[m2lines]: https://m2lines.github.io/
[team]: https://m2lines.github.io/team/

---

## 3. LIBRARIES

Check these **before writing new code**: what you need may already exist. Their modules are in
`references/libraries.md`.

| Library  | For                                                 | Author       | Links                                    |
| -------- | --------------------------------------------------- | ------------ | ---------------------------------------- |
| `azula`  | diffusion models: noise schedule, denoiser, sampler | probabilists | [GitHub][azula-gh], [docs][azula-docs]   |
| `zuko`   | normalizing flows on top of `torch.distributions`   | probabilists | [GitHub][zuko-gh], [docs][zuko-docs]     |
| `shaggy` | training tools, autoencoders, losses                | me           | [GitHub][shaggy-gh], [docs][shaggy-docs] |
| `albus`  | metrics                                             | me           | [GitHub][albus-gh], [docs][albus-docs]   |

[azula-gh]: https://github.com/probabilists/azula
[azula-docs]: https://azula.readthedocs.io
[zuko-gh]: https://github.com/probabilists/zuko
[zuko-docs]: https://zuko.readthedocs.io
[shaggy-gh]: https://github.com/VikVador/Shaggy
[shaggy-docs]: https://shaggy.readthedocs.io
[albus-gh]: https://github.com/VikVador/Albus
[albus-docs]: https://albus-metrics.readthedocs.io

### How to check a library before coding

1. **Read its module table** in `references/libraries.md`: find the module that could hold what you need.
2. **Confirm the API** in its docs (links above) or in the installed source, from the project environment:
   `python -c "import shaggy, os; print(os.path.dirname(shaggy.__file__))"` (same for `albus`, `azula`, `zuko`),
   then read the module there.
3. **Reuse it** when it exists; write new code only for what is missing.

**Good to know**

- The repositories are `VikVador/Shaggy` and `VikVador/Albus` (capitals); the Python packages stay lowercase:
  `import shaggy`, `import albus`.

---

## 4. DOCUMENTATION

| Topic                  | Link                                                                               |
| ---------------------- | ---------------------------------------------------------------------------------- |
| NYU Torch cluster      | [services.rt.nyu.edu](https://services.rt.nyu.edu/docs/hpc/getting_started/intro/) |
| Lucia cluster          | [doc.lucia.cenaero.be](https://doc.lucia.cenaero.be)                               |
| Copernicus Marine data | [data.marine.copernicus.eu](https://data.marine.copernicus.eu)                     |
| OSN (object storage)   | [openstoragenetwork.github.io/docs](https://openstoragenetwork.github.io/docs/)    |
| Weights & Biases       | [wandb.ai/sail-nyu](https://wandb.ai/sail-nyu)                                     |

---

## 5. MONITORING RUNS (WANDB)

You can read my runs on [wandb.ai/sail-nyu](https://wandb.ai/sail-nyu) with the Python API of `wandb`, from the project
environment: the key is already set up on the cluster (`wandb login`), so no setup is needed. Which clusters exactly
is not written down: **[verify]** (§ 6).

| Project                      | Runs                                                        |
| ---------------------------- | ----------------------------------------------------------- |
| `heimdall-training-encoders` | one run per encoder, e.g. `ENC_sst_lc128_tk5650__D9D7_164C` |
| `neptune-training-encoders`  | one run per encoder, e.g. `ENC_surface_lc128_tk576__F3D5`   |

| Logged metric                      | Meaning                  |
| ---------------------------------- | ------------------------ |
| `Training/Loss`, `Validation/Loss` | the losses               |
| `Informations/Learning Rate`       | learning rate (schedule) |
| `Informations/Gradient Norm`       | gradient norm (spikes)   |
| `Informations/Steps Update`        | optimizer updates done   |
| `Informations/Samples Seen`        | samples seen             |

`runs.py` does the reading, with the Python of the project environment, and prints what matters:

```bash
python <skill folder>/runs.py sail-nyu/heimdall-training-encoders              # every run: state, updates, losses, verdict
python <skill folder>/runs.py sail-nyu/heimdall-training-encoders --run <name>  # one run: curves (20 points), diagnostics
```

The verdict names a run that diverged (loss not finite, or 3 times above its minimum), that overfits (validation
rising while training falls) or whose gradient norm spikes. For anything else, the API directly:
`wandb.Api().runs("sail-nyu/<project>")`, then `run.history(keys=[...])`.

### Rules

- **Read only**: never delete, edit, tag or move a run.
- **Never read nor print the key** (`~/.netrc`): the library finds it by itself.
- **If `wandb.Api()` fails or no key is set**: stop and tell me, with the error. Never ask me for the key, print it
  or set it (`wandb login`, `WANDB_API_KEY`): I set it up myself.
- **Use it** to check a training (divergence, overfitting, a run that stopped) and to compare runs with numbers.

---

## 6. OPEN QUESTIONS

| #   | Question                                                     | Status                                                          |
| --- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| 1   | On which clusters is the WandB key set (Torch, Lucia, both)? | **open**, ask me, or check that `wandb.Api()` works on each one |
