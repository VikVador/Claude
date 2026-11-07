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
    "abstract": "The abstract, word for word from the paper page (render.py shows its first lines).",
    "abstract_fr": "A faithful French translation of the same abstract, for the French copy."
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
import decorations  # noqa: E402

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
def config_block(name, block):
    """The flat `block:` of config/<name>.yaml as a dict of strings (standard library only)."""
    text = open(os.path.join(HERE, '..', 'config', f'{name}.yaml'), encoding='utf-8').read()
    m = re.search(rf'^{block}:\s*\n((?:[ \t].*\n|\s*\n)*)', text, re.M)
    out = {}
    for line in (m.group(1) if m else '').splitlines():
        kv = re.match(r'^\s+(\w+):\s*(.*?)\s*(?:#.*)?$', line)
        if kv:
            out[kv.group(1)] = kv.group(2).strip().strip('"\'')
    return out


def settings():
    """Labels and maximum number of papers, read from config/papers.yaml (standard library only)."""
    text = open(os.path.join(HERE, '..', 'config', 'papers.yaml'), encoding='utf-8').read()
    labels = re.findall(r'^\s*- label:\s*"?(.+?)"?\s*(?:#.*)?$', text, re.M)
    cells = int(config_block('papers', 'papers').get('max', 15))
    half = (len(labels) + 1) // 2
    return labels[:half], labels[half:], cells


LEFT, RIGHT, CELLS = settings()  # labels in the order of the config, half per column; one cell per possible paper
ON, OFF = "#c2603d", "#d9dff1"
WORDS = {
    "en": dict(t_issue="Issue", t_new="new papers", t_published="Published"),
    "fr": dict(t_issue="Numéro", t_new="nouveaux papiers", t_published="Publié le"),
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


def excerpt(text, n):
    """The first n characters of an abstract, cut at a word, with an ellipsis (about 5 lines on a computer)."""
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(' ', 1)[0].rstrip(' ,;:.')
    return cut + '…'


def check_papers(c, lang):
    papers, errors = c["papers"], []
    if not 1 <= len(papers) <= CELLS:
        errors.append(f"{len(papers)} papers: must be 1 to {CELLS}")
    if not re.fullmatch(r'\d{3}', str(c.get("issue", ""))):
        errors.append(f"issue {c.get('issue')!r}: three digits, e.g. 042")
    key = "abstract" if lang == "en" else "abstract_fr"
    for i, p in enumerate(papers, 1):
        if p.get("label") not in LEFT + RIGHT:
            errors.append(f"paper {i}: unknown label {p.get('label')!r}")
        if len(p.get(key, "")) < 100:
            errors.append(f"paper {i}: no {key} (or shorter than 100 characters)")
        if not p.get("authors"):
            errors.append(f"paper {i}: no author")
    return errors


def logo(path, width):
    """An SVG file of logos/, inline, at `width` pixels, comments and blank space removed."""
    svg = open(os.path.join(HERE, '..', path), encoding='utf-8').read()
    svg = re.sub(r'<!--.*?-->', '', svg, flags=re.S)
    svg = re.sub(r'>\s+<', '><', re.sub(r'[ \t]{2,}', ' ', svg)).strip()
    vb = [float(x) for x in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    w = int(width)
    return svg.replace('<svg ', f'<svg width="{w}" height="{round(w * vb[3] / vb[2])}" style="display:block;" ', 1)


def papers(src, dst, lang):
    c = json.load(open(src, encoding='utf-8'))
    errors = check_papers(c, lang)
    if errors:
        sys.exit("\n".join(errors))
    look = config_block('papers', 'look')
    chars = int(look.get('abstract_chars', 480))
    counts = {k: 0 for k in LEFT + RIGHT}
    items = []
    for i, p in enumerate(c["papers"], 1):
        counts[p["label"]] += 1
        names = p["authors"][:3]
        items.append({**p, "number": i, "et_al": bool(p.get("et_al")) or len(p["authors"]) > 3,
                      "authors": [{"name": n, "sep": ", " if j < len(names) - 1 else ""} for j, n in enumerate(names)],
                      "published": day(p.get("published", ""), lang, short=True),
                      "abstract": excerpt(p["abstract" if lang == "en" else "abstract_fr"], chars),
                      "bl": decorations.bands("left", i + 1), "br": decorations.bands("right", i + 1)})

    def theme(k):
        return {"label": k, "count": counts[k],
                "cells": [{"colour": ON if j < counts[k] else OFF, "pad": "0" if j == CELLS - 1 else "0 2px 0 0"}
                          for j in range(CELLS)]}

    gap = 28
    ctx = {**WORDS[lang], "lang": lang, "issue": c["issue"], "date": day(c["date"], lang), "count": len(items),
           "papers": items, "themes_left": [theme(k) for k in LEFT], "themes_right": [theme(k) for k in RIGHT],
           "logo": logo(look.get('logo', 'logos/papers.svg'), look.get('logo_width', 150)),
           "logo_width": look.get('logo_width', 150), "gap": gap,
           "frame_width": 640 + 2 * (decorations.BANDS_WIDTH + gap),
           "head_bl": decorations.bands("left", -1), "head_br": decorations.bands("right", -1),
           "stats_bl": decorations.bands("left", 0), "stats_br": decorations.bands("right", 0)}
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


def university(src, dst, deco=None):
    c = json.load(open(src, encoding='utf-8'))
    who = identity()
    style = deco or who.get("decoration", "none")
    draw = decorations.STYLES[style]
    margin, gap = (0, 0) if style == "none" else (decorations.WIDTH, 40)
    narrow, narrow_gap = (0, 0) if style == "none" else (decorations.NARROW, 8)

    def both(side, colour, n, h, h_phone, top, offset):
        """The margin drawn wide (computer) and narrow (phone); the template's <style> shows one of them. Each is as
        tall as its block on that screen (h, h_phone), a little under the real height."""
        wide, css = draw(side, colour, n, h, top, offset)
        small, _ = draw(side, colour, n, h_phone, top, offset, decorations.NARROW)
        if wide == '&nbsp;':
            return wide, css
        return (f'<div class="wide">{wide}</div>'
                f'<div class="narrow" style="display:none; max-height:0; overflow:hidden;">{small}</div>', css)
    titles = {**TITLES, "events": who.get("events_title", TITLES["events"])}
    unescape = lambda s: H.unescape(s) if isinstance(s, str) else s  # noqa: E731  (old files wrote &amp;)
    sections, offset = [], 82  # offset: top of the current block in the email, for decorations.py
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
        # Height of the section, a little under the real one (40 top + title and underline 46 + rows), so that its
        # decoration fills the margin without ever making the section taller.
        rows_h = 52 if not raw else 66 * len(sec["deadlines"]) + sum(r["height"] for r in sec["rows"])
        h, n = 40 + 46 + rows_h - 6, len(sections) + 1
        # On a phone, rows shrink to their text: about 44 px each, under a 77 px title block (measured 2026-11-07).
        h_phone = 77 + (44 * (len(sec["deadlines"]) + len(sec["rows"])) if raw else 38) - 4
        (sec["left"], sec["left_css"]), (sec["right"], sec["right_css"]) = (
            both("left", COLOURS[k], n, h, h_phone, 40, offset), both("right", COLOURS[k], n, h, h_phone, 40, offset))
        offset += h + 6
        sections.append(sec)
    (hl, hl_css), (hr, hr_css) = both("left", HL, 0, 82, 76, 0, 0), both("right", HL, 0, 82, 76, 0, 0)
    size = finish("university", {"week": nodetect(unescape(c["week"])), "sections": sections,
                                 "logo": logo(who["logo"], who.get("logo_width", 150)), "logo_width": who.get("logo_width", "150"),
                                 "margin": margin, "gap": gap, "frame_width": 640 + 2 * (margin + gap),
                                 "narrow": narrow, "narrow_gap": narrow_gap,
                                 "header_left": hl, "header_left_css": hl_css,
                                 "header_right": hr, "header_right_css": hr_css}, dst)
    print(f"OK university: {sum(len(s['deadlines']) + len(s['rows']) for s in sections)} items, {size:.0f} KB, "
          f"decoration {style}, 0 image")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("name", choices=["papers", "university"])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--lang", choices=["en", "fr"], default="en")
    ap.add_argument("--decoration", choices=sorted(decorations.STYLES), help="university: override the config")
    a = ap.parse_args()
    papers(a.src, a.dst, a.lang) if a.name == "papers" else university(a.src, a.dst, a.decoration)
