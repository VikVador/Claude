r"""Collect the candidate papers of the Daily Paper Digest, so that no listing page is read by Claude.

Usage (from plugins/newsletter/):
  python3 scripts/collect.py config/papers.yaml --exclude /tmp/exclude.txt > /tmp/candidates.json

For every `sources` group of the config with `arxiv` or `journals` (the labs have no listing: they stay with the
subagents of the skill), the script reads the arXiv listing pages and Crossref, keeps the titles that contain one of
`collect.domain` and one of `collect.method` (or two method terms), drops the ids of the exclusion list, fetches the authors,
the date and the abstract of the survivors, and prints one JSON:

  {"candidates": [{"source", "group", "id", "doi", "url", "title", "authors", "published", "abstract"}, ...],
   "sources": [{"group", "source", "read", "kept", "error"}, ...]}

`abstract` is empty when Crossref has none: the skill gives those to a subagent. Standard library only (Python 3.6
or later; `yaml` is used when installed). About twenty requests, a minute at most, polite to both APIs.
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from xml.etree import ElementTree

ARXIV_LIST = 'https://arxiv.org/list/{cat}/{page}?skip=0&show=2000'
ARXIV_API = 'http://export.arxiv.org/api/query?id_list={ids}&max_results={n}'
CROSSREF = ('https://api.crossref.org/works?filter={issn},from-pub-date:{since}&query.bibliographic={query}'
            '&select=DOI,title,container-title,published,abstract,author&rows={rows}&mailto={mailto}')
ATOM = '{http://www.w3.org/2005/Atom}'
UA = 'daily-paper-digest/1.0 (mailto:{mailto})'
BATCH = 50  # arXiv ids per API request (the API accepts more; batches keep the answer small)
PAUSE = 3   # seconds between two arXiv API requests, as the API asks


# ---------------------------------------------------------------- config ----------------------------------------------
def load_yaml(path):
    """The config, with PyYAML when installed, else a small reader of the shapes this config uses."""
    text = open(path, encoding='utf-8').read()
    try:
        import yaml
        return yaml.safe_load(text)
    except ImportError:
        return _parse_block(_lines(text), 0)[0]


def _lines(text):
    out = []
    for raw in text.splitlines():
        line = re.sub(r'(^|\s)#.*$', '', raw).rstrip()  # a comment starts the line or follows a space
        if not line.strip():
            continue
        if out and _open(out[-1][1]):  # a flow list or mapping continued on the next line
            out[-1] = (out[-1][0], out[-1][1] + ' ' + line.strip())
        else:
            out.append((len(line) - len(line.lstrip()), line.strip()))
    return out


def _open(line):
    return line.count('[') + line.count('{') > line.count(']') + line.count('}')


def _scalar(v):
    v = v.strip()
    if v.startswith('[') and v.endswith(']'):
        return [_scalar(x) for x in _split(v[1:-1])]
    if v.startswith('{') and v.endswith('}'):
        return {k.strip().strip('"\''): _scalar(w) for k, w in (x.split(':', 1) for x in _split(v[1:-1]) if ':' in x)}
    if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
        return v[1:-1]
    if re.fullmatch(r'-?\d+', v):
        return int(v)
    return {'true': True, 'false': False}.get(v.lower(), v)


def _split(s):
    """Split a flow list or mapping on the commas outside quotes and brackets."""
    parts, depth, quote, cur = [], 0, '', ''
    for c in s:
        if quote:
            quote = '' if c == quote else quote
        elif c in '"\'':
            quote = c
        elif c in '[{':
            depth += 1
        elif c in ']}':
            depth -= 1
        if c == ',' and depth == 0 and not quote:
            parts.append(cur)
            cur = ''
        else:
            cur += c
    return [p for p in parts + [cur] if p.strip()]


def _parse_block(lines, i):
    """Parse the block starting at line i (a mapping or a list); return (value, next line index)."""
    indent = lines[i][0]
    if lines[i][1].startswith('- '):
        out = []
        while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith('- '):
            item = lines[i][1][2:].strip()
            if re.match(r'^\w[\w ]*:(\s|$)', item) and not item.startswith(('{', '[')):
                # a mapping written on the item line: re-read it as a block of its own
                lines[i] = (indent + 2, item)
                value, i = _parse_block(lines, i)
            else:
                value, i = _scalar(item), i + 1
            out.append(value)
        return out, i
    out = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith('- '):
        key, _, rest = lines[i][1].partition(':')
        rest, i = rest.strip(), i + 1
        if rest in ('>', '|'):
            parts = []
            while i < len(lines) and lines[i][0] > indent:
                parts.append(lines[i][1])
                i += 1
            out[key.strip()] = ' '.join(parts)
        elif rest == '' and i < len(lines) and lines[i][0] > indent:
            out[key.strip()], i = _parse_block(lines, i)
        else:
            out[key.strip()] = _scalar(rest) if rest else None
    return out, i


# ---------------------------------------------------------------- reading ---------------------------------------------
def get(url, mailto):
    request = urllib.request.Request(url, headers={'User-Agent': UA.format(mailto=mailto)})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode('utf-8', 'replace')


def arxiv_listing(cat, page, mailto):
    """(id, title) of every paper of one listing page."""
    html = get(ARXIV_LIST.format(cat=cat, page=page), mailto)
    ids = re.findall(r'<a href ?="/abs/(\d{4}\.\d{4,5})" title="Abstract"', html)
    titles = [re.sub(r'\s+', ' ', unescape(t)).strip()
              for t in re.findall(r"<div class='list-title mathjax'>\s*<span class='descriptor'>Title:</span>(.*?)</div>",
                                  html, re.S)]
    return list(zip(ids, titles))


def arxiv_metadata(ids, mailto):
    """Authors, date and abstract of arXiv papers, from the API, in batches."""
    out = {}
    for k in range(0, len(ids), BATCH):
        batch = ids[k:k + BATCH]
        if k:
            time.sleep(PAUSE)
        root = ElementTree.fromstring(get(ARXIV_API.format(ids=','.join(batch), n=len(batch)), mailto))
        for entry in root.iter(ATOM + 'entry'):
            arxiv_id = re.search(r'(\d{4}\.\d{4,5})', entry.findtext(ATOM + 'id', '')).group(1)
            out[arxiv_id] = {
                'authors': [a.findtext(ATOM + 'name', '').strip() for a in entry.iter(ATOM + 'author')],
                'published': entry.findtext(ATOM + 'published', '')[:10],
                'abstract': re.sub(r'\s+', ' ', entry.findtext(ATOM + 'summary', '')).strip(),
            }
    return out


def crossref(issns, since, queries, rows, mailto):
    """The works of some journals since a date matching one of short queries (a long one returns nothing)."""
    items = {}
    for k, query in enumerate(queries):
        url = CROSSREF.format(issn=','.join('issn:' + i for i in issns), since=since,
                              query=urllib.parse.quote_plus(query), rows=rows, mailto=urllib.parse.quote(mailto))
        if k:
            time.sleep(1)
        try:
            answer = get(url, mailto)
        except urllib.error.HTTPError as error:
            if error.code != 429:
                raise
            time.sleep(10)
            answer = get(url, mailto)
        for item in json.loads(answer)['message']['items']:
            items.setdefault(item.get('DOI', ''), item)
    return list(items.values())


def jats_text(xml):
    """The plain text of a Crossref abstract (JATS XML or plain), without its 'Abstract' title."""
    text = re.sub(r'<jats:title>.*?</jats:title>', ' ', xml or '', flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', unescape(text)).strip()
    return re.sub(r'^Abstract\.?\s*', '', text)


# ---------------------------------------------------------------- collection ------------------------------------------
def collect(config, exclude):
    cfg = load_yaml(config)
    today = dt.date.today()
    mailto = _decode(cfg.get('crossref_mailto', '')) or 'nobody@example.org'
    collect_cfg = cfg.get('collect') or {}
    domain = [re.compile(r'\b' + re.escape(str(t).lower())) for t in collect_cfg.get('domain', [])]
    method = [re.compile(r'\b' + re.escape(str(t).lower())) for t in collect_cfg.get('method', [])]
    windows = cfg.get('windows_days') or {}

    def relevant(title):
        t = title.lower()
        methods = sum(1 for p in method if p.search(t))
        return (methods >= 1 and any(p.search(t) for p in domain)) or methods >= 2

    excluded = lambda *ids: any(i and i.lower() in exclude for i in ids)  # noqa: E731
    candidates, report = [], []

    for source in cfg.get('sources') or []:
        group = source.get('group', '')
        if 'arxiv' in source:
            since = today - dt.timedelta(days=int(windows.get('arxiv', 30)))
            months = sorted({(today.replace(day=1) - dt.timedelta(days=1)).strftime('%Y-%m'), today.strftime('%Y-%m')})
            pages = [(c, m) for c in source['arxiv'].get('monthly', []) for m in months]
            pages += [(c, 'recent') for c in source['arxiv'].get('recent', [])]
            kept = {}
            for cat, page in pages:
                try:
                    papers, before = arxiv_listing(cat, page, mailto), len(kept)
                    for arxiv_id, title in papers:
                        if relevant(title) and not excluded(arxiv_id, '10.48550/arXiv.' + arxiv_id):
                            kept.setdefault(arxiv_id, (title, cat))
                    report.append({'group': group, 'source': f'arXiv {cat} ({page})', 'read': len(papers),
                                   'kept': len(kept) - before, 'error': ''})
                except Exception as error:  # noqa: BLE001
                    report.append({'group': group, 'source': f'arXiv {cat} ({page})', 'read': 0, 'kept': 0,
                                   'error': f'{type(error).__name__}: {error}'})
            try:
                meta = arxiv_metadata(sorted(kept), mailto) if kept else {}
            except Exception as error:  # noqa: BLE001
                meta = {}
                report.append({'group': group, 'source': 'arXiv API (metadata)', 'read': 0, 'kept': 0,
                               'error': f'{type(error).__name__}: {error}'})
            for arxiv_id, (title, cat) in kept.items():
                m = meta.get(arxiv_id, {})
                if m.get('published') and m['published'] < since.isoformat():
                    continue
                candidates.append({'source': f'arXiv {cat}', 'group': group, 'id': arxiv_id,
                                   'doi': '10.48550/arXiv.' + arxiv_id, 'url': 'https://arxiv.org/abs/' + arxiv_id,
                                   'title': title, 'authors': m.get('authors', []),
                                   'published': m.get('published', ''), 'abstract': m.get('abstract', '')})
        elif 'journals' in source:
            since = (today - dt.timedelta(days=int(windows.get('journals', 90)))).isoformat()
            journals = source['journals']
            queries = [str(t) for t in (cfg.get('keywords') or {}).get('domain', ['ocean'])]
            try:
                items = crossref([str(j['issn']) for j in journals], since, queries,
                                 int(collect_cfg.get('crossref_rows', 100)), mailto)
            except Exception as error:  # noqa: BLE001
                report.append({'group': group, 'source': ', '.join(j['name'] for j in journals), 'read': 0,
                               'kept': 0, 'error': f'{type(error).__name__}: {error}'})
                continue
            kept = 0
            for item in items:
                title = re.sub(r'\s+', ' ', unescape(' '.join(item.get('title') or []))).strip()
                doi = item.get('DOI', '')
                if not title or not relevant(title) or excluded(doi):
                    continue
                parts = (item.get('published') or {}).get('date-parts', [[]])[0] + [1, 1]
                authors = [' '.join(x for x in (a.get('given'), a.get('family')) if x) for a in item.get('author', [])]
                candidates.append({'source': ' '.join(item.get('container-title') or [''])[:60], 'group': group,
                                   'id': doi, 'doi': doi, 'url': 'https://doi.org/' + doi, 'title': title,
                                   'authors': authors, 'published': '%04d-%02d-%02d' % tuple(parts[:3]),
                                   'abstract': jats_text(item.get('abstract'))})
                kept += 1
            report.append({'group': group, 'source': ', '.join(j['name'] for j in journals), 'read': len(items),
                           'kept': kept, 'error': ''})
    return {'candidates': candidates, 'sources': report}


def _decode(value):
    import base64
    try:
        return base64.b64decode(str(value).strip(), validate=True).decode('utf-8')
    except Exception:  # noqa: BLE001
        return str(value).strip()


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('config', help='config/papers.yaml')
    ap.add_argument('--exclude', help='file with one excluded id per line (state.py exclude)')
    a = ap.parse_args()
    ids = set()
    if a.exclude:
        ids = {line.strip().lower() for line in open(a.exclude, encoding='utf-8') if line.strip()}
    result = collect(a.config, ids)
    json.dump(result, sys.stdout, indent=1, ensure_ascii=False)
    print()
    print(f"{len(result['candidates'])} candidates, "
          f"{sum(1 for c in result['candidates'] if not c['abstract'])} without abstract, "
          f"{sum(1 for s in result['sources'] if s['error'])} sources in error", file=sys.stderr)
