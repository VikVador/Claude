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


# ---------------------------------------------------------------- Daily Paper Digest -----------------------------------
# Small scientific figures in the digest's colours, one per block, at the top of its margin. Same signature as above.
DIGEST = ["#c2603d", "#d58a6f", "#e7b9a6", "#4a5169", "#8f95aa", "#c5cde6"]


def histogram(side, colour, i, height, top, offset=0, width=WIDTH):
    """Histogrammes: the logo's histogram turned on its side, bars growing from the outer edge towards the content."""
    rng = random.Random(f'histogram-{side}-{i}')
    bar, gap = 3, 2
    n = min(20, int((min(height, 130) - 8) // (bar + gap)))
    mu1, mu2 = rng.uniform(.2, .45) * n, rng.uniform(.55, .85) * n
    body = ''
    for k in range(n):
        v = math.exp(-((k - mu1) / (n * .12)) ** 2) + .7 * math.exp(-((k - mu2) / (n * .1)) ** 2)
        length = max(2, v * (width - 10) * .9)
        x = 4 if side == 'left' else width - 4 - length
        c = DIGEST[0] if v > .75 else DIGEST[1] if v > .45 else DIGEST[2] if v > .2 else DIGEST[5]
        body += f'<rect x="{x:.0f}" y="{4 + k * (bar + gap)}" width="{length:.0f}" height="{bar}" fill="{c}"/>'
    return svg(height, body, width), ''


def scatter(side, colour, i, height, top, offset=0, width=WIDTH):
    """Nuage de points: noisy observations around one slow fitted curve that runs down the whole margin, from the
    header to the last paper (offset places each block on the same curve), drawn over the full height of the block."""
    rng = random.Random(f'scatter-{side}-{i}')
    phase = 0 if side == 'left' else math.pi
    a = width * .26
    xs = lambda y: width / 2 + a * math.sin(phase + (offset + y) / 95)  # noqa: E731
    path = ' '.join(f'{"M" if k == 0 else "L"}{xs(y):.0f},{y}' for k, y in enumerate(range(0, int(height) + 1, 14)))
    body = f'<path d="{path}" fill="none" stroke="{DIGEST[3]}" stroke-width="1.1" stroke-opacity=".45"/>'
    groups = {c: '' for c in DIGEST[:3]}  # one <g fill> per colour: shorter than a fill on every point
    y = rng.uniform(2, 10)
    while y < height - 3:
        x = min(max(xs(y) + rng.gauss(0, width * .1), 3), width - 3)
        groups[rng.choice(DIGEST[:3])] += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rng.choice([1.5, 2, 2.5])}"/>'
        y += rng.uniform(12, 28)
    body += ''.join(f'<g fill="{c}">{pts}</g>' for c, pts in groups.items() if pts)
    return svg(height, body, width), ''




def density(side, colour, i, height, top, offset=0, width=WIDTH):
    """Densité: a two-bump probability density drawn along the margin, filled, with a rug of samples on its axis."""
    rng = random.Random(f'density-{side}-{i}')
    h = min(height, 130) - 8
    m1, m2, w2 = rng.uniform(.2, .4), rng.uniform(.6, .8), rng.uniform(.5, .9)
    pdf = lambda t: math.exp(-((t - m1) / .1) ** 2) + w2 * math.exp(-((t - m2) / .08) ** 2)  # noqa: E731
    base = 4 if side == 'left' else width - 4
    sign = 1 if side == 'left' else -1
    pts = [(base + sign * pdf(k / 24) * (width - 14) * .85, 4 + k / 24 * h) for k in range(25)]
    d = f'M{base},4 ' + ' '.join(f'L{x:.0f},{y:.0f}' for x, y in pts) + f' L{base},{4 + h:.0f} Z'
    body = (f'<path d="{d}" fill="{DIGEST[2]}" fill-opacity=".55" stroke="{DIGEST[0]}" stroke-width="1.2"/>'
            f'<rect x="{base - (1 if side == "left" else 0):.1f}" y="4" width="1" height="{h:.1f}" fill="{DIGEST[4]}"/>')
    for _ in range(9):
        t = rng.gauss(m1, .07) if rng.random() < .6 else rng.gauss(m2, .06)
        if 0 < t < 1:
            body += f'<rect x="{base - sign * 6 - (0 if side == "left" else 4):.0f}" y="{4 + t * h:.0f}" width="4" height="1" fill="{DIGEST[3]}"/>'
    return svg(height, body, width), ''


def signal(side, colour, i, height, top, offset=0, width=WIDTH):
    """Signal: a vertical time series with its samples, like a sensor or a forecast trace."""
    rng = random.Random(f'signal-{side}-{i}')
    h = min(height, 130) - 8
    x, pts = width / 2, []
    for k in range(int(h // 6) + 1):
        x = min(max(x + rng.gauss(0, width * .08) - (x - width / 2) * .25, 4), width - 4)
        pts.append((x, 4 + k * 6))
    d = ' '.join(f'{"M" if k == 0 else "L"}{px:.0f},{py:.0f}' for k, (px, py) in enumerate(pts))
    body = f'<path d="{d}" fill="none" stroke="{DIGEST[0]}" stroke-width="1.3" stroke-linejoin="round"/>'
    body += ''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="1.5" fill="{DIGEST[3]}"/>' for k, (px, py) in enumerate(pts) if k % 3 == 0)
    return svg(height, body, width), ''


# ---------------------------------------------------------------- continuous, high-tech --------------------------------
# Each runs down the whole margin: positions use the global height offset + y, so a block continues the previous one.
# Shapes are packed into a few <path> elements per colour (Gmail clips an email above 102 KB).
INK, SOFT, ACCENT, ACCENT2 = "#4a5169", "#c5cde6", "#c2603d", "#e7b9a6"


def _rng(name, side, k):
    return random.Random(f'{name}-{side}-{k}')


def network(side, colour, i, height, top, offset=0, width=WIDTH):
    """Réseau de neurones: layers of neurons every 44 px, each linked to some neurons of the next layer."""
    step, cols = 44, [width * .25, width * .5, width * .75]
    first = math.ceil(offset / step)
    layers = {}
    for k in range(first, int((offset + height) // step) + 1):
        r = _rng('network', side, k)
        layers[k] = [x for x in cols if r.random() < .8] or [cols[1]]
    edges, on, off = '', '', ''
    for k, xs in layers.items():
        y = k * step - offset
        r = _rng('network-edges', side, k)
        if k + 1 in layers:
            for x in xs:
                for x2 in r.sample(layers[k + 1], min(len(layers[k + 1]), r.choice([1, 2]))):
                    edges += f'M{x:.0f},{y:.0f}L{x2:.0f},{y + step:.0f}'
        for x in xs:
            dot = f'M{x - 3:.0f},{y:.0f}a3,3 0 1,0 6,0a3,3 0 1,0 -6,0'
            if r.random() < .3:
                on += dot
            else:
                off += dot
    body = (f'<path d="{edges}" stroke="{SOFT}" stroke-width="1"/><path d="{off}" fill="#ffffff" stroke="{INK}" '
            f'stroke-width="1"/><path d="{on}" fill="{ACCENT}"/>')
    return svg(height, body, width), ''


def mesh(side, colour, i, height, top, offset=0, width=WIDTH):
    """Grille de modèle: a curvilinear ocean-model grid, its lines bent by a slow flow, a few cells highlighted."""
    warp = lambda x, y: x + 5 * math.sin((offset + y) / 80 + x / 20)  # noqa: E731
    v = ''
    for x in (width * .2, width * .5, width * .8):
        v += 'M' + 'L'.join(f'{warp(x, y):.0f},{y}' for y in range(0, int(height) + 1, 12))
    h, cells, step = '', '', 22
    for k in range(math.ceil(offset / step), int((offset + height) // step) + 1):
        y = k * step - offset
        h += f'M{warp(width * .2, y):.0f},{y:.0f}L{warp(width * .8, y):.0f},{y:.0f}'
        r = _rng('mesh', side, k)
        if r.random() < .22 and y + step <= height:
            x0 = width * (.2 if r.random() < .5 else .5)
            cells += (f'M{warp(x0, y):.0f},{y:.0f}L{warp(x0 + width * .3, y):.0f},{y:.0f}'
                      f'L{warp(x0 + width * .3, y + step):.0f},{y + step:.0f}L{warp(x0, y + step):.0f},{y + step:.0f}Z')
    body = (f'<path d="{cells}" fill="{ACCENT2}" fill-opacity=".7"/>'
            f'<path d="{v}{h}" fill="none" stroke="{SOFT}" stroke-width="1"/>')
    return svg(height, body, width), ''


def circuit(side, colour, i, height, top, offset=0, width=WIDTH):
    """Circuit imprimé: two thin traces running down the whole margin, changing lane at 45° now and then, a small via at
    each end of a turn. Each trace is drawn once for the whole email (positions from the top of the email) and every
    block shows its own slice of it, so the lines join from one block to the next."""
    lanes = [width * .3, width * .55, width * .8] if side == 'left' else [width * .2, width * .45, width * .7]
    step, jog = 56, 14
    body = ''
    for t, (stroke, start) in enumerate(((SOFT, 0), (ACCENT, 2))):
        r = random.Random(f'circuit-{side}-{t}')
        lane, y, pts, vias = start, -step, [], ''
        while y < offset + height + step:
            nxt = lane
            if r.random() < .3:
                nxt = min(max(lane + r.choice([-1, 1]), 0), len(lanes) - 1)
            if nxt != lane and offset - step < y < offset + height + step:
                for yy, ll in ((y, lane), (y + jog, nxt)):
                    vias += f'M{lanes[ll] - 2:.1f},{yy - offset:.0f}a2,2 0 1,0 4,0a2,2 0 1,0 -4,0'
            if offset - 2 * step < y < offset + height + 2 * step:
                pts.append((lanes[lane], y - offset))
                if nxt != lane:
                    pts.append((lanes[nxt], y + jog - offset))
            if nxt != lane:
                y += jog
            lane, y = nxt, y + step
        d = 'M' + 'L'.join(f'{x:.0f},{yy:.0f}' for x, yy in pts)
        body += (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.2" stroke-linejoin="round"/>'
                 f'<path d="{vias}" fill="#ffffff" stroke="{stroke}" stroke-width="1.1"/>')
    return svg(height, body, width), ''


def streamlines(side, colour, i, height, top, offset=0, width=WIDTH):
    """Champ de vecteurs: small arrows of a swirling current, as a numerical model's output."""
    arrows, step = {INK: '', ACCENT: ''}, 18
    for k in range(math.ceil(offset / step), int((offset + height) // step) + 1):
        y = k * step - offset
        for x in ((width * .3,) if k % 2 else (width * .7,)):
            gy = offset + y
            ang = math.sin(gy / 70) * 1.6 + math.cos(x / 25)
            mag = 6 + 4 * abs(math.sin(gy / 110))
            dx, dy = mag * math.cos(ang), mag * math.sin(ang)
            hx, hy = math.cos(ang + 2.6) * 3, math.sin(ang + 2.6) * 3
            gx, gy2 = math.cos(ang - 2.6) * 3, math.sin(ang - 2.6) * 3
            c = ACCENT if mag > 8.5 else INK
            arrows[c] += (f'M{x - dx / 2:.0f},{y - dy / 2:.0f}l{dx:.0f},{dy:.0f}'
                          f'm{hx:.0f},{hy:.0f}l{-hx:.0f},{-hy:.0f}l{gx:.0f},{gy2:.0f}')
    body = ''.join(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.2" stroke-linecap="round"/>'
                   for c, d in arrows.items() if d)
    return svg(height, body, width), ''


def diffusion(side, colour, i, height, top, offset=0, width=WIDTH):
    """Diffusion: samples along a curve, alternately noised and denoised as one goes down, like a diffusion model."""
    phase = 0 if side == 'left' else math.pi
    xs = lambda gy: width / 2 + width * .25 * math.sin(phase + gy / 90)  # noqa: E731
    pts = {ACCENT: '', ACCENT2: '', INK: ''}
    curve, step = '', 13
    for k in range(math.ceil(offset / step), int((offset + height) // step) + 1):
        y = k * step - offset
        gy = offset + y
        noise = (1 + math.cos(gy / 160)) / 2          # 0: clean, 1: pure noise
        r = _rng('diffusion', side, k)
        x = min(max(xs(gy) + r.gauss(0, 1) * noise * width * .3, 2), width - 2)
        c = INK if noise > .66 else ACCENT2 if noise > .33 else ACCENT
        pts[c] += f'M{x - 2:.0f},{y:.0f}a2,2 0 1,0 4,0a2,2 0 1,0 -4,0'
        if noise < .3:
            curve += f'{"M" if not curve or curve.endswith("|") else "L"}{xs(gy):.0f},{y:.0f}'
        elif curve and not curve.endswith('|'):
            curve += '|'
    body = f'<path d="{curve.replace("|", "")}" fill="none" stroke="{SOFT}" stroke-width="1"/>'
    body += ''.join(f'<path d="{d}" fill="{c}"/>' for c, d in pts.items() if d)
    return svg(height, body, width), ''


def latent(side, colour, i, height, top, offset=0, width=WIDTH):
    """Tenseur latent: a column of small cells shaded like a feature map, its pattern drifting down the margin."""
    shades = [ACCENT, "#d58a6f", ACCENT2, SOFT, "#eaeffc"]
    paths, step, size = {c: '' for c in shades}, 11, 7
    for k in range(math.ceil(offset / step), int((offset + height) // step) + 1):
        y = k * step - offset
        if y + size > height:
            break
        gy = offset + y
        for c_i, x in enumerate((width * .3, width * .3 + 10, width * .3 + 20)):
            v = (math.sin(gy / 45 + c_i * 1.3) + math.sin(gy / 17 - c_i) * .5 + 1.5) / 3
            if v < .25:
                continue
            c = shades[min(4, int((1 - v) * 5))]
            paths[c] += f'M{x:.0f},{y:.0f}h{size}v{size}h-{size}z'
    body = ''.join(f'<path d="{d}" fill="{c}"/>' for c, d in paths.items() if d)
    return svg(height, body, width), ''


STYLES.update({"histogram": histogram, "scatter": scatter, "density": density, "signal": signal,
               "network": network, "mesh": mesh, "circuit": circuit, "streamlines": streamlines,
               "diffusion": diffusion, "latent": latent})
CONTINUOUS = {"scatter", "network", "mesh", "circuit", "streamlines", "diffusion", "latent"}
