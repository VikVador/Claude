"""State of the Daily Paper Digest: what was sent, what is kept for later, who receives it.

Usage (from plugins/newsletter/):
  python3 scripts/state.py status                   next issue, sent today?, last dominant labels, back-up size
  python3 scripts/state.py exclude                  every id already sent, one per line (the strict exclusion list)
  python3 scripts/state.py recipients <en|fr> [--not a@b.c ...]
                                                    active subscribers of one language, one per line
  python3 scripts/state.py record content.json      append the issue to data/papers/sent.json and replace
                                                    data/papers/backup.json by content.json "backup"

Files: data/papers/sent.json, data/papers/backup.json, data/subscribers.yaml. Standard library only.
"""
import argparse
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


def subscribers():
    """Parse data/subscribers.yaml: a list of {email, active, language}, the only shape it ever has."""
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
            cur[m.group(2)] = m.group(3).strip().strip('"\'')
    return out


def recipients(lang, skip):
    seen = {s.lower() for s in skip}
    for s in subscribers():
        email = s.get('email', '').strip()
        if (s.get('active', '').lower() == 'true' and s.get('language', 'en').lower() == lang
                and EMAIL.match(email) and email.lower() not in seen):
            seen.add(email.lower())
            print(email)


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
    sub.add_parser('status')
    sub.add_parser('exclude')
    r = sub.add_parser('recipients')
    r.add_argument('lang', choices=['en', 'fr'])
    r.add_argument('--not', dest='skip', nargs='*', default=[])
    sub.add_parser('record').add_argument('src')
    a = ap.parse_args()
    {'status': status, 'exclude': exclude}.get(a.cmd, lambda: None)()
    if a.cmd == 'recipients':
        recipients(a.lang, a.skip)
    if a.cmd == 'record':
        record(a.src)
