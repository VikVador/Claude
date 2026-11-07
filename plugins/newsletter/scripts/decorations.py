"""Margin decorations of the university newsletter, drawn in the left and right margins of every block.

Each style is a function (side, colour, index, height, top) -> (HTML of one margin cell, CSS of that cell):
- `height` is the height of the block (header or section) the margin sits next to, estimated by render.py a little
  under the real one, so that a decoration never makes a block taller;
- `top` is the white space above the block's content (40 px above a section, 0 for the header);
- `offset` is where the block starts from the top of the email, so that a pattern can flow across blocks;
- `width` is the margin width: WIDTH on a computer, NARROW on a phone (render.py draws both, the template shows one).
Pick the style with
`university.decoration` in config/university.yaml; `none` draws nothing.
"""
import math
import random

WIDTH = 64   # margin width in pixels, on a computer
NARROW = 24  # margin width on a phone (under 600 px)

# The colours of the logo, from logos/uliege.svg
PALETTE = ["#ffda55", "#f8bd35", "#f39435", "#ec5a39", "#a6c770", "#80bd49", "#36a657", "#008d88",
           "#00768b", "#008598", "#78aeb6", "#5995bb", "#273d80", "#71549a", "#afa0c6"]


def tint(colour, t):
    """Mix a colour with white: t = 0 keeps it, t = 1 gives white."""
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02x%02x%02x' % tuple(round(c + (255 - c) * t) for c in (r, g, b))


def svg(height, body, width=WIDTH):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" style="display:block;" aria-hidden="true">{body}</svg>')


def triangle(x, y, s, right):
    """A half-diamond like those of the logo, pointing right or left, of height s."""
    if right:
        return f'{x:.1f},{y:.1f} {x + s * .87:.1f},{y + s / 2:.1f} {x:.1f},{y + s:.1f}'
    return f'{x + s * .87:.1f},{y:.1f} {x + s * .87:.1f},{y + s:.1f} {x:.1f},{y + s / 2:.1f}'


# ---------------------------------------------------------------- styles ----------------------------------------------
def shards(side, colour, i, height, top, offset=0, width=WIDTH):
    """Éclats: triangles of the logo palette all along the margin, one about every 22 px, drifting gently around a
    slow wave so that the margins read as one continuous trail from the header to the last section; sizes and
    opacities vary a little, and every block and side has its own draw."""
    rng = random.Random(f'shards-{side}-{i}')
    phase = 0 if side == 'left' else math.pi                         # same wave in every block: no break
    f = width / WIDTH                                                 # 1 on a computer, smaller on a phone
    body, y = '', rng.uniform(2, 10)
    while True:
        s = rng.choice([6, 8, 9, 11, 12, 14, 16]) * max(f, .65)
        if y + s > height - 2:
            break
        centre = width / 2 + 13 * f * math.sin(phase + (offset + y) / 70)  # the slow wave the trail follows
        x = min(max(centre + rng.uniform(-9, 9) * f - s * .43, 2), width - s * .87 - 2)
        body += (f'<polygon points="{triangle(x, y, s, rng.random() < .5)}" fill="{rng.choice(PALETTE)}" '
                 f'fill-opacity="{rng.choice([.45, .6, .75, .9])}"/>')
        y += rng.uniform(15, 27) * max(f, .8)
    return svg(height, body, width), ''


def ribbon(side, colour, i, height, top, offset=0, width=WIDTH):
    """Ruban: a thin vertical line along the content, in the colour of the section, from top to bottom."""
    edge = 'right' if side == 'left' else 'left'
    return '&nbsp;', f'border-{edge}:3px solid {tint(colour, .35)};'


def column(side, colour, i, height, top, offset=0, width=WIDTH):
    """Colonne: a column of triangles in shades of the section colour, like the logo, fading downwards."""
    f = width / WIDTH
    x0 = (30 if side == 'left' else 8) * f
    rows = max(0, min(8, (height - top - 16) // 9))
    body = ''
    for row in range(rows):
        for col in range(2):
            y = top + 4 + row * 9 + col * 4.5
            body += (f'<polygon points="{triangle(x0 + col * 13 * f, y, 9 * max(f, .6), (row + col) % 2 == 0)}" '
                     f'fill="{tint(colour, .15 + .1 * ((row + col) % 3))}" fill-opacity="{1 - row * .88 / rows:.2f}"/>')
    return svg(height, body, width), ''


def waves(side, colour, i, height, top, offset=0, width=WIDTH):
    """Vagues: three thin vertical waves in the section colour, for the ocean."""
    steps = max(1, min(8, (height - top - 8) // 22))
    body = ''
    f = width / WIDTH
    for k, x in enumerate((18, 32, 46)):
        x *= f
        pts = ' '.join(f'{x + 5 * f * (1 if (j + k) % 2 else -1):.1f},{top + 4 + j * 22}' for j in range(steps + 1))
        body += (f'<polyline points="{pts}" fill="none" stroke="{tint(colour, .2 + .2 * k)}" stroke-width="1.6" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
    return svg(height, body, width), ''


def none(side, colour, i, height, top, offset=0, width=WIDTH):
    return '&nbsp;', ''


STYLES = {"shards": shards, "ribbon": ribbon, "column": column, "waves": waves, "none": none}


# ---------------------------------------------------------------- bands (Daily Paper Digest) --------------------------
# Thin vertical bands in the margins, like the lines of a spectrum or a data stream. They are table cells with a
# background colour, so they always run the full height of their row, on any screen. From the outside in:
# (width, kind, zone); "band" cells get a colour, "gap" cells stay white; "out" cells (class o) disappear on a
# phone, "in" cells (class i) stay.
BAND_LAYOUT = [(6, "gap", "out"), (2, "band", "out"), (7, "gap", "out"), (1, "band", "out"), (6, "gap", "out"),
               (3, "band", "in"), (5, "gap", "in"), (1, "band", "in"), (4, "gap", "in"), (2, "band", "in")]
BAND_PALETTE = ["#c2603d", "#d58a6f", "#e7b9a6", "#4a5169", "#8f95aa", "#c5cde6", "#9a4424"]
BAND_OFF = .3  # chance that a band is blank in a row: the gaps give the rhythm


def bands(side, i):
    """The cells of one margin for row i: [{w, c, cls}], outside first on the left, mirrored on the right. Next white
    cells of the same zone are merged into one, to keep the email small (Gmail clips it above 102 KB)."""
    rng = random.Random(f'bands-{side}-{i}')
    cells = []
    for w, kind, zone in BAND_LAYOUT:
        c = "#ffffff" if kind == "gap" or rng.random() < BAND_OFF else rng.choice(BAND_PALETTE)
        cls = "o" if zone == "out" else "i"
        if cells and c == "#ffffff" and cells[-1]["c"] == c and cells[-1]["cls"] == cls:
            cells[-1]["w"] += w
        else:
            cells.append({"w": w, "c": c, "cls": cls})
    return cells if side == 'left' else cells[::-1]


BANDS_WIDTH = sum(w for w, _, _ in BAND_LAYOUT)
