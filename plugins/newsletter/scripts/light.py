"""Force an HTML email to stay light in every mail client (no automatic dark mode).

1. Adds the color-scheme metas and style to the <head>.
2. Gives every <body>, <table> and <td> an explicit bgcolor and background-color: its own colour if it has one,
   otherwise the colour of the nearest ancestor that has one (white at the top), so that clients which recolour
   "transparent" areas have nothing left to recolour.

Same file in every newsletter skill: change both copies together.
"""
import re

HEAD = ('<meta name="color-scheme" content="light only">'
        '<meta name="supported-color-schemes" content="light">'
        '<style>:root{color-scheme:light only;supported-color-schemes:light}</style>')
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
PAINT = {"body", "table", "td"}
WHITE = "#ffffff"


def _own_bg(tag):
    """Colour set on the tag itself (style background-color, else bgcolor), or None."""
    style = re.search(r'style="([^"]*)"', tag)
    if style:
        m = re.search(r'background-color:\s*(#[0-9a-fA-F]{3,6})', style.group(1))
        if m:
            return m.group(1)
    m = re.search(r'bgcolor="(#[0-9a-fA-F]{3,6})"', tag)
    return m.group(1) if m else None


def _paint(tag, name, colour):
    tag = re.sub(r'\sbgcolor="[^"]*"', '', tag)
    tag = tag.replace(f'<{name}', f'<{name} bgcolor="{colour}"', 1)
    if re.search(r'style="', tag):
        if not re.search(r'background-color:', re.search(r'style="([^"]*)"', tag).group(1)):
            tag = tag.replace('style="', f'style="background-color:{colour};', 1)
    else:
        tag = tag.replace(f'<{name} bgcolor="{colour}"', f'<{name} bgcolor="{colour}" style="background-color:{colour};"', 1)
    return tag


def force_light(html):
    html = re.sub(r'<meta name="(color-scheme|supported-color-schemes)"[^>]*>', '', html)
    html = re.sub(r'<style>:root\{color-scheme[^<]*</style>', '', html)
    html = html.replace('</head>', HEAD + '</head>', 1) if '</head>' in html else HEAD + html
    out, stack = [], []  # stack of (tag name, background colour in force)
    for tok in re.split(r'(<[^>]+>)', html):
        m = re.match(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)', tok)
        if not m or tok.startswith('<!'):
            out.append(tok)
            continue
        closing, name = m.group(1) == '/', m.group(2).lower()
        if closing:
            while stack:
                if stack.pop()[0] == name:
                    break
            out.append(tok)
            continue
        inherited = stack[-1][1] if stack else WHITE
        colour = _own_bg(tok) or inherited
        if name in PAINT:
            tok = _paint(tok, m.group(2), colour)
        if name not in VOID and not tok.endswith('/>'):
            stack.append((name, colour))
        out.append(tok)
    return ''.join(out)
