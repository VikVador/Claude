"""State of the newsletters: who receives them, what was sent, what is kept for later.

Usage (from plugins/newsletter/):
  python3 scripts/state.py plan config/<newsletter>.yaml
                          who gets which email, one per language (JSON): each person only in the language they
                          chose; the owner gets the reports and is the only recipient in test mode
  python3 scripts/state.py encode <address>         the base64 to write in data/subscribers.yaml
  python3 scripts/state.py decode <base64>          the address back
  python3 scripts/state.py status                   papers digest: next issue, sent today?, last dominant labels
  python3 scripts/state.py exclude                  papers digest: every id already sent, one per line
  python3 scripts/state.py record content.json      papers digest: append the issue to data/papers/sent.json and
                                                    replace data/papers/backup.json by content.json "backup"

Files: data/subscribers.yaml, data/papers/sent.json, data/papers/backup.json. Standard library only.
"""
import argparse
import base64
import collections
import datetime as dt
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SENT = os.path.join(ROOT, 'data', 'papers', 'sent.json')
BACKUP = os.path.join(ROOT, 'data', 'papers', 'backup.json')
SUBSCRIBERS = os.path.join(ROOT, 'data', 'subscribers.yaml')
EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$')


def load(path, default):
    return json.load(open(path, encoding='utf-8')) if os.path.exists(path) else default


def dump(path, value):
    """JSON with one paper per line: readable in a diff, still plain JSON."""
    if isinstance(value, list) and value and isinstance(value[0], dict) and 'papers' in value[0]:
        blocks = []
        for it in value:
            papers = ',\n'.join('    ' + json.dumps(p, ensure_ascii=False) for p in it['papers'])
            blocks.append(f'  {{"issue": "{it["issue"]}", "date": "{it["date"]}", "papers": [\n{papers}\n  ]}}')
        text = '[\n' + ',\n'.join(blocks) + '\n]\n'
    else:
        text = '[\n' + ',\n'.join('  ' + json.dumps(p, ensure_ascii=False) for p in value) + '\n]\n' if value else '[]\n'
    json.loads(text)  # never write a broken file
    open(path, 'w', encoding='utf-8').write(text)


def dominant(issue):
    c = collections.Counter(p['label'] for p in issue['papers'])
    return c.most_common(1)[0][0] if c else None


def today():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo('America/New_York')).date().isoformat()
    except Exception:
        return dt.date.today().isoformat()


def status():
    sent = load(SENT, [])
    last = sent[-1]['issue'] if sent else '000'
    print(json.dumps({
        'next_issue': f'{int(last) + 1:03d}',
        'today': today(),
        'already_sent_today': any(it['date'] == today() for it in sent),
        'last_two_dominant_labels': [dominant(it) for it in sent[-2:]],
        'papers_sent': sum(len(it['papers']) for it in sent),
        'backup': len(load(BACKUP, [])),
    }, indent=1))


def exclude():
    for it in load(SENT, []):
        for p in it['papers']:
            if p['id'] and p['id'].lower() not in ('non disponible', 'not available'):
                print(p['id'].lower())


def encode(address):
    return base64.b64encode(address.strip().encode('utf-8')).decode('ascii')


def decode(value):
    try:
        return base64.b64decode(value.strip(), validate=True).decode('utf-8')
    except Exception:
        return value.strip()  # written in clear by mistake: still usable


def scalar(v):
    v = v.strip().strip('"\'')
    if v.startswith('[') and v.endswith(']'):
        return [x.strip().strip('"\'') for x in v[1:-1].split(',') if x.strip()]
    return {'true': True, 'false': False}.get(v.lower(), v)


def subscribers():
    """Parse data/subscribers.yaml: a list of {email, newsletters, language, active, owner}, its only shape."""
    out, cur = [], None
    for line in open(SUBSCRIBERS, encoding='utf-8'):
        line = line.split('#', 1)[0].rstrip()
        m = re.match(r'^\s*(-\s+)?(\w+):\s*(.*)$', line)
        if not m or m.group(2) == 'subscribers':
            continue
        if m.group(1):
            cur = {}
            out.append(cur)
        if cur is not None:
            cur[m.group(2)] = scalar(m.group(3))
    for s in out:
        s['email'] = decode(str(s.get('email', '')))
        n = s.get('newsletters', [])
        s['newsletters'] = n if isinstance(n, list) else [n]
    return out


def sending(config):
    """The `sending:` block of a config YAML, as a flat dict."""
    text = open(config, encoding='utf-8').read()
    block = re.search(r'^sending:\s*\n((?:[ \t].*\n|\s*\n)*)', text, re.M)
    out = {}
    for line in (block.group(1) if block else '').splitlines():
        m = re.match(r'^\s+(\w+):\s*(.*?)\s*(?:#.*)?$', line)
        if m:
            out[m.group(1)] = scalar(m.group(2))
    return out


def plan(config):
    cfg = sending(config)
    name, test, cap = cfg['newsletter'], cfg.get('test', True), int(cfg.get('max_bcc', 49))
    fixed = cfg.get('language')  # a newsletter written in one language only
    subs = [s for s in subscribers() if s.get('active') is True and name in s['newsletters']
            and EMAIL.match(s['email'])]
    owners = [s for s in subs if s.get('owner') is True]
    if not owners:
        sys.exit(f"no active owner subscribed to {name!r} in data/subscribers.yaml")
    owner = owners[0]
    lang_of = lambda s: fixed or s.get('language', 'en')  # noqa: E731
    emails, seen = {lang_of(owner): []}, {owner['email'].lower()}
    cut = []
    if not test:
        for s in subs:
            if s['email'].lower() in seen:
                continue
            seen.add(s['email'].lower())
            bcc = emails.setdefault(lang_of(s), [])
            (bcc if len(bcc) < cap else cut).append(s['email'])
    # Everyone gets only the language they chose. The owner is in `to` of their own language's email; an email in
    # another language goes `to` the sender address itself, its readers all in `bcc`.
    sender = re.search(r'<([^>]+)>', str(cfg.get('from', ''))) or re.search(r'(\S+@\S+)', str(cfg.get('from', '')))
    sender = sender.group(1) if sender else owner['email']
    print(json.dumps({'newsletter': name, 'test': test, 'owner': owner['email'],
                      'emails': [{'language': k, 'to': [owner['email'] if k == lang_of(owner) else sender], 'bcc': v}
                                 for k, v in emails.items()],
                      'cut': cut}, indent=1, ensure_ascii=False))


def record(src):
    c = json.load(open(src, encoding='utf-8'))
    sent = load(SENT, [])
    if any(it['issue'] == c['issue'] for it in sent):
        sys.exit(f"issue {c['issue']} is already in sent.json: nothing written")
    papers = [{'id': p.get('doi') or p.get('id') or 'non disponible', 'title': p['title'],
               'link': p.get('url', ''), 'label': p['label']} for p in c['papers']]
    sent.append({'issue': c['issue'], 'date': c.get('date', today()), 'papers': papers})
    dump(SENT, sent)
    dump(BACKUP, c.get('backup', []))
    print(f"OK issue {c['issue']}: {len(papers)} papers recorded, {len(c.get('backup', []))} in back-up")


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('plan').add_argument('config')
    sub.add_parser('encode').add_argument('address')
    sub.add_parser('decode').add_argument('value')
    sub.add_parser('status')
    sub.add_parser('exclude')
    sub.add_parser('record').add_argument('src')
    a = ap.parse_args()
    if a.cmd == 'plan':
        plan(a.config)
    elif a.cmd == 'encode':
        print(encode(a.address))
    elif a.cmd == 'decode':
        print(decode(a.value))
    elif a.cmd == 'record':
        record(a.src)
    else:
        {'status': status, 'exclude': exclude}[a.cmd]()
