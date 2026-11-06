---
name: animation
description: Use before drawing a diagram or an animation that explains how a mechanism, an architecture or a probabilistic concept works (attention, cross-attention, convolution and receptive fields, graph networks, U-Net, encoders, autoencoders and VAEs, normalizing flows, diffusion models, stochastic interpolants, distributions and their transformations), on its own or in a report. Gives the style to follow, the one of the figures of the book Understanding Deep Learning (Prince, 2023), with the book's figures as examples, and a small library to draw tensors, modules and arrows and to play them step by step.
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Animation: show what happens inside a mechanism,
     ┌─┴───┴─┐       tensor by tensor, in the style of a textbook.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# ANIMATION

A diagram of a mechanism shows **what happens inside**: which tensors exist, their shapes, which ones are combined and
how, step by step. Simplify the sizes, never the mechanism. The model to follow is the book of **Simon J. D. Prince,
Understanding Deep Learning** (MIT Press, 2023), whose figures are clear and precise: always look at its examples
first, and credit it when a diagram follows one of its figures.

This is **the default for explaining an architecture** to a reader with a background in deep learning and
mathematics: show the tensors and how they are computed. **Follow the book's way of showing, not its exact look**:
the colours are lighter and cleaner here (a pale teal panel, the palette of the report), and another style is welcome
when it explains a point better (a map for a spatial mechanism, a timeline for a pipeline).

| File          | What                                                                                     |
| ------------- | ---------------------------------------------------------------------------------------- |
| `examples.md` | the figures of the book kept as examples (images in `examples/`), what each one teaches  |
| `diagram.js`  | helpers: tensors as grids, modules, labels, arrows, heat map, step-by-step player        |

Results (curves, maps, measures) are not diagrams: they follow the `figure` skill. A diagram in a report follows the
`report` skill for the page, and this one for the drawing.

---

## 1. BEFORE DRAWING

1. Write down the mechanism as equations, with the shape of every tensor (e.g. `\mathbf{Q} = \boldsymbol\beta_q
   \mathbf{1}^T + \boldsymbol\Omega_q\mathbf{X}`, of shape `D \times N`). If a shape is unknown, find it before drawing.
2. Open the closest examples of `examples.md` with the Read tool: `TransformerBlockSA.png` (matrix form of
   attention), `Conv2D.png` (grids and sliding), `ConvNetworkRF.png` (receptive fields across layers),
   `FlowIntro.png` (a density through a map), `DiffusionDensity.png` (a density over time), `AppJointMarg.png`
   (a joint and its marginals).
3. Decide the steps: one operation per step, in the order of the computation.

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
    { text: "<strong>Queries.</strong> … \\(\\mathbf{Q} = \\boldsymbol\\Omega_q\\mathbf{X}\\) …", draw: (tick) => {} },
  ]);
  });
</script>
```

Copy `diagram.js` next to the body of the report: `build.py` of the report skill inlines it. The page style
(`style.css` of the report skill) sizes the drawing and the player.

## 5. CREDIT

When a diagram follows a figure of the book, say so in its caption: "d'après Prince (2023), chapitre 12", and add
the book to the sources: `Prince, S. J. D. (2023). Understanding Deep Learning. The MIT Press.
https://udlbook.github.io/udlbook/`. The figures in `examples/` are the author's, under CC BY-NC-ND 4.0: shown
unmodified, never redrawn as our own.
