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

1. Write down the mechanism as equations, with the shape of every tensor (e.g. `Q = β_q 1ᵀ + Ω_q X_o`, shape
   `D × N_o`). If a shape is unknown, find it before drawing.
2. Open the closest examples of `examples.md` with the Read tool: `TransformerBlockSA.png` (matrix form of
   attention), `Conv2D.png` (grids and sliding), `ConvNetworkRF.png` (receptive fields across layers).
3. Decide the steps: one operation per step, in the order of the computation.

## 2. STYLE (FROM THE BOOK)

| Element        | How                                                                                                |
| -------------- | -------------------------------------------------------------------------------------------------- |
| Tensor         | a grid of white cells with thin black lines, one column per token (shape `D × N`, as in the book)  |
| Dimensions     | the symbols of the shape on the grid: `N` above, `D` on the left, in italic serif                  |
| Name, equation | under each tensor: its name, then its equation in semibold (`Q = β_q 1ᵀ + Ω_q X`)                  |
| Module         | the operation inside a rounded pale teal panel, its name in the top right ("Cross-attention")     |
| Arrows         | thin black lines turning at right angles, from the tensor used to the tensor computed             |
| Weights        | attention weights or kernel values as a white-to-brown heat map                                    |
| Focus          | the elements used at this step in light grey-blue or orange; the rest of the diagram faded         |
| Neurons, nodes | circles, with their name inside when useful (`x₁₁`, `h₂₃`); layers as orange columns of circles    |
| Receptive field| a light grey wedge from the field in one layer to the unit it feeds in the next                     |
| Symbols        | ⊗ for a product, ⊕ for a sum, at the place where the operation happens                             |
| Densities      | filled curves on a shared axis: teal for the base or source, orange for the target or model        |
| Samples        | small arrows or points on the axis, followed through the map that moves them                       |
| Time           | downwards, as in the diffusion figures; paths as thin coloured lines, one colour per sample        |
| Marginals      | the density over (x, t) as a white-to-brown heat map, with slices at a few times beside it         |
| Joint, 2D      | a heat map of the joint, its two marginals drawn along the axes                                    |

- **Real sizes are written, toy sizes are drawn**: draw 4 to 8 tokens and channels, and give the real numbers.
- **Every diagram translates its dimensions** in a small legend on the drawing (`Diagram.legend`): what each symbol
  means (channels, tokens, i.e. the flattened spatial grid Y × X, time, ensemble members) and its real size, and the
  total size of the main tensors: "D: channels of a token, 768 · N_o: ocean tokens, the 63 × 135 latent grid
  flattened, 8 505 · X_o: 768 × 8 505 values". The book's names (D for channels, N for tokens) are kept; the legend
  links them to the project's (C, T, Y × X).
- Same tensor, same position and same name in every step; same colour for the same role in the whole report.
- Text in the drawing: short names and symbols only (13 to 14 px at the drawn scale); explanations go in the step text.
- Mathematical symbols in italic serif, as in the book (the only italic allowed by the report skill).

## 3. ANIMATION

- **Step by step, like the panels a), b), c), d) of the book**: each step adds or highlights one operation; what is
  not used at this step is faded, not hidden, so that the whole mechanism stays in view.
- **Inside a step**, a short loop may sweep one element at a time (one query column, one output cell, the kernel
  sliding), to show that the same operation repeats.
- Each step has a text of one or two sentences: what is computed, its shape, why. Bilingual in a report.
- Controls: previous, next, play / pause (`Diagram.player`). It plays by itself, unless the reader prefers reduced
  motion; any click on previous or next stops it.
- Hand-written inline SVG drawn by a small script, no library, no external image: `diagram.js` gives the pieces.
  The drawing is at least 600 px wide: on a phone, it scrolls sideways rather than shrinking below legibility.

## 4. CODE

```html
<figure><div class="plate" id="anim"></div><figcaption>…</figcaption></figure>
<script src="diagram.js"></script>
<script>
  const s = Diagram.svg(document.getElementById("anim"), 720, 440, "Cross-attention, step by step");
  Diagram.panel(s, 150, 20, 410, 400, "Cross-attention");
  const X = Diagram.grid(s, { x: 30, y: 70, rows: 4, cols: 6, top: "N", left: "D" });
  Diagram.label(s, X.x + X.w / 2, X.y + X.h + 20, ["Input", "X"]);
  Diagram.player(document.getElementById("anim"), [{ text: "…", draw: (tick) => {} }]);
</script>
```

Copy `diagram.js` next to the body of the report: `build.py` of the report skill inlines it. The page style
(`style.css` of the report skill) sizes the drawing and the player.

## 5. CREDIT

When a diagram follows a figure of the book, say so in its caption: "d'après Prince (2023), chapitre 12", and add
the book to the sources: `Prince, S. J. D. (2023). Understanding Deep Learning. The MIT Press.
https://udlbook.github.io/udlbook/`. The figures in `examples/` are the author's, under CC BY-NC-ND 4.0: shown
unmodified, never redrawn as our own.
