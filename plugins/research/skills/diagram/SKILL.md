---
name: diagram
description: "Use before drawing a diagram or a step-by-step animation that explains how a mechanism, an architecture or a probabilistic concept works (attention, convolutions and receptive fields, graph networks, U-Net, autoencoders and VAEs, normalizing flows, diffusion models, stochastic interpolants, distributions), for a report, a slide or on its own. Gives the style of the figures of Understanding Deep Learning (Prince, 2023), with the book's figures as examples, and diagram.js to draw tensors, modules and arrows and play them step by step. Not for plots of data or results (figure skill)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Diagram: show what happens inside a mechanism, 
     ┌─┴───┴─┐       tensor by tensor, in the style of a textbook.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# DIAGRAM

A diagram of a mechanism shows **what happens inside**: which tensors exist, their shapes, which ones are combined and
how, step by step. Simplify the sizes, never the mechanism. The model to follow is the book of **Simon J. D. Prince,
Understanding Deep Learning** (MIT Press, 2023), whose figures are clear and precise: always look at its examples
first, and credit it when a diagram follows one of its figures.

This is **the default for explaining an architecture** to a reader with a background in deep learning and
mathematics: show the tensors and how they are computed. **Follow the book's way of showing, not its exact look**:
the colours are lighter and cleaner here (a pale teal panel, the palette of the report), and another style is welcome
when it explains a point better (a map for a spatial mechanism, a timeline for a pipeline).

| File          | Use                                                                          | When                          |
| ------------- | ---------------------------------------------------------------------------- | ----------------------------- |
| `examples.md` | **Read**: the figures of the book (images in `examples/`), what each teaches | before every diagram (§ 1)    |
| `diagram.js`  | **Copy** next to the body: tensors as grids, modules, labels, arrows, player | when drawing (§ 4)            |

Related: the `figure` skill for results (curves, maps, measures); the `report` skill for the page around a diagram.

**Contents**

0. In short
1. Before drawing
2. Style (from the book)
3. Animation
4. Code
5. Credit
6. Check

---

## 0. IN SHORT

1. **Equations and shapes first**: write the mechanism as equations with the shape of every tensor (§ 1).
2. **Open the closest example of the book** before drawing (§ 1), and follow its way of showing.
3. **One operation per step**, the rest faded, never hidden; same tensor, same place, same name in every step.
4. **A legend of the dimensions** at the bottom of every drawing; all mathematics in LaTeX.
5. **Simplify the sizes, never the mechanism**: toy sizes (4 to 8 tokens and channels).
6. **Look at the result** before showing it (§ 6), and credit the book when a diagram follows one of its figures.

---

## 1. BEFORE DRAWING

1. Write down the mechanism as equations, with the shape of every tensor (e.g. `\mathbf{Q} = \boldsymbol\beta_q
   \mathbf{1}^T + \boldsymbol\Omega_q\mathbf{X}`, of shape `D \times N`). If a shape is unknown, find it before drawing.
2. Open the closest examples of `examples.md` with the Read tool: `TransformerBlockSA.png` (matrix form of
   attention), `Conv2D.png` (grids and sliding), `ConvNetworkRF.png` (receptive fields across layers),
   `FlowIntro.png` (a density through a map), `DiffusionDensity.png` (a density over time), `AppJointMarg.png`
   (a joint and its marginals).
3. Decide the steps: one operation per step, in the order of the computation.

---

## 2. STYLE (FROM THE BOOK)

| Element        | How                                                                                                |
| -------------- | -------------------------------------------------------------------------------------------------- |
| Tensor         | a grid of white cells with thin black lines, one column per token (shape `D × N`, as in the book)  |
| Dimensions     | the symbols of the shape on the grid, in LaTeX: `N` above, `D` on the left                         |
| Name, equation | under each tensor: its name, then its equation in LaTeX, matrices in bold                          |
| Module         | the operation inside a rounded pale teal panel, its name in the top right ("Cross-attention")     |
| Arrows         | thin black lines turning at right angles, from the tensor used to the tensor computed             |
| Weights        | attention weights or kernel values as a white-to-brown heat map                                    |
| Focus          | the elements used at this step in light grey-blue or orange; the rest of the diagram faded         |
| Neurons, nodes | circles, with their name inside when useful (`$x_{11}$`, `$h_{23}$`); layers as columns of circles |
| Receptive field| a light grey wedge from the field in one layer to the unit it feeds in the next                     |
| Symbols        | `$\otimes$` for a product, `$\oplus$` for a sum, at the place where the operation happens         |
| Densities      | filled curves on a shared axis: teal for the base or source, orange for the target or model        |
| Samples        | small arrows or points on the axis, followed through the map that moves them                       |
| Time           | downwards, as in the diffusion figures; paths as thin coloured lines, one colour per sample        |
| Marginals      | the density over (x, t) as a white-to-brown heat map, with slices at a few times beside it         |
| Joint, 2D      | a heat map of the joint, its two marginals drawn along the axes                                    |

- **Toy sizes are drawn**: 4 to 8 tokens and channels, enough to see the mechanism.
- **Every diagram explains its dimensions** in a legend at the bottom of the drawing (`Diagram.legend`): the title
  "Legend", a thin rule, then the items one after the other over the width, wrapping only when a line is full. One
  item per symbol, a few plain words each, and the shapes of the main tensors, all mathematics in LaTeX, e.g.
  `["D", "channels of a token"]`, `["N", "tokens"]`, `"$\\mathbf{X}$, $\\mathbf{Q}$: $D \\times N$"`.
  Nothing more: no project, no long explanation; the text of the step says the rest. The book's names are kept (D
  for channels, N for tokens).
- **General, never tied to a project**: the instructions and the examples of this skill stay general; a diagram made
  for a project names its own tensors, but the drawing explains the mechanism, not the project.
- Same tensor, same position and same name in every step; same colour for the same role in the whole report.
- Text in the drawing: short names and symbols only (13 to 14 px at the drawn scale); explanations go in the step text.
- **All mathematics in LaTeX**, as in the text of the report: in the drawing, `$…$` inside any label or legend
  (`Diagram.rich`, `Diagram.tex`, rendered by MathJax), e.g. `"$\\mathbf{Q} = \\boldsymbol\\Omega_q\\mathbf{X}$"`; in the step texts, `\\( … \\)`. Matrices in bold, as in the book.
- Draw inside `Diagram.ready(() => { … })`, so that MathJax is loaded before the labels are typeset.

---

## 3. ANIMATION

- **Step by step, like the panels a), b), c), d) of the book**: each step adds or highlights one operation; what is
  not used at this step is faded, not hidden, so that the whole mechanism stays in view.
- **Inside a step**, a short loop may sweep one element at a time (one query column, one output cell, the kernel
  sliding), to show that the same operation repeats.
- Each step has a text: a short title in semibold, then one or two sentences on what is computed, its shape, why;
  mathematics in LaTeX (`\\( … \\)`); bilingual in a report.
- **Layout, top to bottom**, in one light frame: the controls, a thin rule, the text of the current step on a light
  shade, then the drawing with its legend at the bottom. Below the frame, directly, the caption of the figure.
- **Controls** (`Diagram.player`), icons with a tooltip, no words: previous, a progress bar to jump to any step,
  next, a toggle for going through the steps, play / pause of the animation inside the current step, and a restart
  that plays everything again from the first step. A toggle is dark when on. It plays by itself, unless the reader
  prefers reduced motion; moving the bar or clicking previous or next pauses the going through the steps.
- Hand-written inline SVG drawn by a small script, no library, no external image: `diagram.js` gives the pieces.
  The drawing is at least 600 px wide: on a phone, it scrolls sideways rather than shrinking below legibility.

---

## 4. CODE

```html
<figure><div class="plate" id="anim"></div><figcaption>…</figcaption></figure>
<script src="diagram.js"></script>
<script>
  Diagram.ready(() => {
  const s = Diagram.svg(document.getElementById("anim"), 720, 500, "Self-attention, step by step");
  Diagram.panel(s, 150, 20, 410, 400, "Self-attention");
  const X = Diagram.grid(s, { x: 30, y: 70, rows: 4, cols: 6, top: "N", left: "D" });
  Diagram.label(s, X.x + X.w / 2, X.y + X.h + 20, ["Input,", "$\\mathbf{X}$"]);
  Diagram.legend(s, 30, 450, [["D", "channels of a token"], ["N", "tokens"], "$\\mathbf{X}$: $D \\times N$"]);
  Diagram.player(document.getElementById("anim"), [
    { text: "<span lang='fr'><strong>Requêtes.</strong> …</span><span lang='en'><strong>Queries.</strong> …</span>", draw: (tick) => {} },
  ]);
  });
</script>
```

Copy `diagram.js` next to the body of the report: `build.py` of the report skill inlines it. The page style
(`style.css` of the report skill) sizes the drawing and the player.

- **On its own**: a report with one section, built with `build.py` of the `report` skill (it loads MathJax and the
  style the drawing needs).
- **On a slide**: a still diagram, exported as SVG or PNG into the talk's `figures/`. A played animation in a deck
  has no tested path yet: ask me.

---

## 5. CREDIT

When a diagram follows a figure of the book, say so in its caption: "d'après Prince (2023), chapitre 12", and add
the book to the sources: `Prince, S. J. D. (2023). Understanding Deep Learning. The MIT Press.
https://udlbook.github.io/udlbook/`. The figures in `examples/` are the author's, under CC BY-NC-ND 4.0: they may
be shown unmodified with this credit, never edited. A diagram drawn here may follow the way a figure shows a
mechanism ("d'après Prince"), never copy the figure itself.

---

## 6. CHECK

Open the built page and look at every step before showing it:

- [ ] the labels and the legend are typeset (no raw `$…$`), nothing overlaps, the drawing is 600 px wide or more;
- [ ] every step draws, the faded parts stay visible, the player buttons work;
- [ ] the step texts exist in French and in English (in a report), and the caption says what the diagram shows.
