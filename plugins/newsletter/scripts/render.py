"""Render a newsletter: content.json -> email HTML, checked and forced light.

Usage:
  python3 render.py papers content.json digest.html --lang en|fr
  python3 render.py university contenu.json newsletter.html

The HTML structure lives in ../templates/<name>.html; this script only fills it. On a problem it prints the list of
problems and exits with 1: fix the JSON and run again, never edit the HTML by hand.

papers content.json (plain text everywhere: render.py escapes & < > itself):
{
  "model": "Opus 5.5", "issue": "038", "date": "2026-11-07",
  "papers": [{
    "url": "https://arxiv.org/abs/2611.01234", "title": "...",
    "authors": ["First Author", "Second Author", "Third Author"], "et_al": true,
    "doi": "10.48550/arXiv.2611.01234", "doi_url": "https://doi.org/10.48550/arXiv.2611.01234",
    "published": "2026-11-05", "label": "ASSIMILATION",
    "summary": "English paragraph with 2 to 5 **key phrases** in bold.",
    "summary_fr": "Le même résumé en français, avec ses **phrases clés**."
  }],
  "backup": [ ... same fields, the candidates kept for the next issue ... ]
}

university contenu.json: see the newsletter-university skill (week, deadlines, seminars, workshops, events, brief, infos).
"""
import argparse
import datetime as dt
import html as H
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from light import force_light  # noqa: E402

TEMPLATES = os.path.join(HERE, '..', 'templates')
MAX_KB = 100  # Gmail clips emails above 102 KB


# ---------------------------------------------------------------- mustache --------------------------------------------
def fill(tpl, ctx):
    """Minimal mustache: {{x}} escaped, {{{x}}} raw, {{#x}}..{{/x}} list or truthy, {{^x}}..{{/x}} falsy."""
    sec = re.compile(r'\{\{([#^])(\w+)\}\}(.*?)\{\{/\2\}\}', re.S)

    def block(m):
        kind, key, inner = m.group(1), m.group(2), m.group(3)
        val = ctx.get(key)
        if kind == '^':
            return fill(inner, ctx) if not val else ''
        if isinstance(val, list):
            return ''.join(fill(inner, {**ctx, **item}) for item in val)
        return fill(inner, ctx) if val else ''

    prev = None
    while prev != tpl:
        prev, tpl = tpl, sec.sub(block, tpl, count=1)
    tpl = re.sub(r'\{\{\{(\w+)\}\}\}', lambda m: str(ctx.get(m.group(1), '')), tpl)
    return re.sub(r'\{\{(\w+)\}\}', lambda m: H.escape(str(ctx.get(m.group(1), '')), quote=False), tpl)


def finish(name, ctx, dst):
    tpl = open(os.path.join(TEMPLATES, f'{name}.html'), encoding='utf-8').read()
    out = re.sub(r'<!--(?!\[if).*?-->', '', fill(tpl, ctx), flags=re.S)
    out = force_light(re.sub(r'>\s+<', '><', out).strip())
    left = re.findall(r'\{\{[^}]*\}\}', out)
    size = len(out.encode('utf-8')) / 1024
    if left or size > MAX_KB:
        sys.exit(f"left placeholders: {left[:5]}; size {size:.0f} KB (max {MAX_KB})")
    open(dst, 'w', encoding='utf-8').write(out)
    return size


# ---------------------------------------------------------------- papers ----------------------------------------------
def settings():
    """Labels and maximum number of papers, read from config/papers.yaml (standard library only)."""
    text = open(os.path.join(HERE, '..', 'config', 'papers.yaml'), encoding='utf-8').read()
    labels = re.findall(r'^\s*- label:\s*"?(.+?)"?\s*(?:#.*)?$', text, re.M)
    block = re.search(r'^papers:\s*\n((?:[ \t].*\n|\s*\n)*)', text, re.M)
    cells = int(re.search(r'^\s+max:\s*(\d+)', block.group(1), re.M).group(1)) if block else 15
    half = (len(labels) + 1) // 2
    return labels[:half], labels[half:], cells


LEFT, RIGHT, CELLS = settings()  # labels in the order of the config, half per column; one cell per possible paper
ON, OFF = "#c2603d", "#d9dff1"
STRONG = '<strong style="color:#1a1f2e;">'
WORDS = {
    "en": dict(t_issue="Issue", t_new="new papers", t_published="Published", t_created="Created by",
               t_powered="and powered by Claude"),
    "fr": dict(t_issue="Numéro", t_new="nouveaux papiers", t_published="Publié le", t_created="Créé par",
               t_powered="avec Claude"),
}
MONTHS = {
    "en": "January February March April May June July August September October November December".split(),
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split(),
}
SHORT = {"en": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
         "fr": "janv. févr. mars avr. mai juin juil. août sept. oct. nov. déc.".split()}


def day(iso, lang, short=False):
    """'2026-11-07' -> '7 November 2026' / '7 novembre 2026'; short: '7 Nov 2026' / '7 nov. 2026'."""
    try:
        d = dt.date.fromisoformat(iso)
    except ValueError:
        return iso  # already written out, or "non disponible"
    return f"{d.day} {(SHORT if short else MONTHS)[lang][d.month - 1]} {d.year}"


def check_papers(c, lang):
    papers, errors = c["papers"], []
    if not 1 <= len(papers) <= CELLS:
        errors.append(f"{len(papers)} papers: must be 1 to {CELLS}")
    if not re.fullmatch(r'\d{3}', str(c.get("issue", ""))):
        errors.append(f"issue {c.get('issue')!r}: three digits, e.g. 042")
    key = "summary" if lang == "en" else "summary_fr"
    for i, p in enumerate(papers, 1):
        if p.get("label") not in LEFT + RIGHT:
            errors.append(f"paper {i}: unknown label {p.get('label')!r}")
        s = p.get(key, "")
        if not s:
            errors.append(f"paper {i}: no {key}")
        if '—' in s or '–' in s:
            errors.append(f"paper {i}: em or en dash in {key}")
        n = len(s.replace('**', ''))
        if s and not 280 <= n <= 750:
            errors.append(f"paper {i}: {key} of {n} characters, aim 300 to 650")
        if s and not 2 <= s.count('**') // 2 <= 5:
            errors.append(f"paper {i}: {s.count('**') // 2} bold key phrases in {key}, need 2 to 5")
        if not p.get("authors"):
            errors.append(f"paper {i}: no author")
    return errors


def papers(src, dst, lang):
    c = json.load(open(src, encoding='utf-8'))
    errors = check_papers(c, lang)
    if errors:
        sys.exit("\n".join(errors))
    counts = {k: 0 for k in LEFT + RIGHT}
    items = []
    for i, p in enumerate(c["papers"], 1):
        counts[p["label"]] += 1
        names = p["authors"][:3]
        summary = H.escape(p["summary" if lang == "en" else "summary_fr"], quote=False)
        items.append({**p, "number": i, "et_al": bool(p.get("et_al")) or len(p["authors"]) > 3,
                      "authors": [{"name": n, "sep": ", " if j < len(names) - 1 else ""} for j, n in enumerate(names)],
                      "published": day(p.get("published", ""), lang, short=True),
                      "summary": re.sub(r'\*\*(.+?)\*\*', lambda m: STRONG + m.group(1) + '</strong>', summary)})

    def theme(k):
        return {"label": k, "count": counts[k],
                "cells": [{"colour": ON if j < counts[k] else OFF, "pad": "0" if j == CELLS - 1 else "0 2px 0 0"}
                          for j in range(CELLS)]}

    ctx = {**WORDS[lang], "lang": lang, "model": c.get("model", ""), "issue": c["issue"],
           "date": day(c["date"], lang), "count": len(items), "papers": items,
           "themes_left": [theme(k) for k in LEFT], "themes_right": [theme(k) for k in RIGHT]}
    size = finish("papers", ctx, dst)
    print(f"OK {lang}: {len(items)} papers, {size:.0f} KB, dominant label {max(counts, key=counts.get)}")


# ---------------------------------------------------------------- university ------------------------------------------
ORDER = ["deadlines", "seminars", "workshops", "events", "brief", "infos"]
TITLES = {"deadlines": "À ne pas manquer", "seminars": "Séminaires & talks", "workshops": "Workshops & conférences",
          "events": "Événements", "brief": "En bref", "infos": "Infos pratiques"}
COLOURS = {"deadlines": "#F48245", "seminars": "#00707F", "workshops": "#FAA919", "events": "#0066B2",
           "brief": "#2CA449", "infos": "#585EA9"}
EMPTY = {"deadlines": "Aucune date limite dans les 10 prochains jours.",
         "seminars": "Rien à signaler pour le moment : je n'ai trouvé aucun séminaire dans tes domaines à travers mes recherches.",
         "workshops": "Rien à signaler pour le moment : je n'ai trouvé aucun workshop ni conférence dans tes domaines à travers mes recherches.",
         "events": "Aucun événement à venir cette semaine.", "brief": "Rien de particulier cette semaine.",
         "infos": "Aucune info pratique cette semaine."}
SPEC = {"seminars": (96, 1, True), "workshops": (92, 2, True), "events": (92, 2, True),
        "brief": (66, 1, True), "infos": (66, 1, False)}  # row height, description lines, first line bold
HL, MUTED = "#00707F", "#6B7480"


def nodetect(t):
    """An invisible character after each number: the iPhone no longer turns dates into underlined links."""
    return re.sub(r'(\d+)', '\\1&zwnj;', H.escape(t, quote=False))


def identity():
    """The `university:` block of config/university.yaml (standard library only)."""
    text = open(os.path.join(HERE, '..', 'config', 'university.yaml'), encoding='utf-8').read()
    block = re.search(r'^university:\s*\n((?:[ \t].*\n|\s*\n)*)', text, re.M)
    out = {}
    for line in (block.group(1) if block else '').splitlines():
        m = re.match(r'^\s+(\w+):\s*(.*?)\s*(?:#.*)?$', line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"\'')
    return out


def university(src, dst):
    c = json.load(open(src, encoding='utf-8'))
    who = identity()
    titles = {**TITLES, "events": who.get("events_title", TITLES["events"])}
    unescape = lambda s: H.unescape(s) if isinstance(s, str) else s  # noqa: E731  (old files wrote &amp;)
    sections = []
    for k in ORDER:
        raw = [{f: unescape(v) for f, v in it.items()} for it in (c.get(k) or [])]
        sec = {"key": k, "title": titles[k], "colour": COLOURS[k], "empty": not raw, "empty_text": EMPTY[k],
               "deadlines": [], "rows": []}
        for i, it in enumerate(raw):
            sep = '' if i == 0 else 'border-top:1px solid #E3E6EB;'
            if k == "deadlines":
                sec["deadlines"].append({**it, "date": nodetect(it["date"]), "sep": sep})
                continue
            height, nl, bold = SPEC[k]
            lines = [{"text": nodetect(it["left"][0]), "br": "", "colour": HL if bold else MUTED,
                      "weight": "font-weight:600;" if bold else ""}]
            lines += [{"text": H.escape(x, quote=False), "br": "<br>", "colour": MUTED, "weight": ""}
                      for x in it["left"][1:]]
            if it.get("reg"):
                lines.append({"text": "Inscription", "br": "<br>", "colour": HL, "weight": ""})
            sec["rows"].append({**it, "link": it.get("link") or "#", "sep": sep, "height": height,
                                "lines": lines, "speaker": it.get("speaker", ""), "desc_mt": 4 if nl > 1 else 2})
        sections.append(sec)
    size = finish("university", {"week": nodetect(unescape(c["week"])), "sections": sections,
                                 "logo_big": who.get("logo_big", ""), "logo_small": who.get("logo_small", ""),
                                 "footer": who.get("footer", "")}, dst)
    print(f"OK university: {sum(len(s['deadlines']) + len(s['rows']) for s in sections)} items, {size:.0f} KB, 0 image")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("name", choices=["papers", "university"])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lang", choices=["en", "fr"], default="en")
    a = ap.parse_args()
    papers(a.src, a.dst, a.lang) if a.name == "papers" else university(a.src, a.dst)
