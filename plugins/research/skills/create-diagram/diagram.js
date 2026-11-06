// Helpers to draw mechanisms in the style of Understanding Deep Learning (Prince, 2023), as inline SVG.
// Tensors are grids with their dimensions, modules are pale teal panels, arrows turn at right angles, weights are a
// white-to-brown heat map, mathematics is LaTeX rendered by MathJax, and a player goes through the steps.
// Load it with a script tag pointing to this file: build.py of the create-report skill inlines it.
const Diagram = (() => {
  const NS = "http://www.w3.org/2000/svg";
  const COLORS = {
    panel: "#e3f1ef", panelLine: "#7db7af", line: "#1a1a1a", faded: 0.15,
    focus: "#c3cad6", query: "#e8710a",
  };

  // Create an SVG element with its attributes, appended to a parent when given
  const el = (tag, attrs = {}, parent = null) => {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (parent) parent.append(e);
    return e;
  };

  // A drawing area of fixed coordinates, scaled to the width of its container
  const svg = (parent, width, height, label) => {
    const s = el("svg", { viewBox: `0 0 ${width} ${height}`, role: "img", "aria-label": label, class: "diagram" }, parent);
    const defs = el("defs", {}, s);
    const marker = el("marker", { id: "arrow", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 7, markerHeight: 7, orient: "auto" }, defs);
    el("path", { d: "M0,0 L10,5 L0,10 z", fill: COLORS.line }, marker);
    return s;
  };

  // A module: teal rounded panel with its name in the top right corner
  const panel = (parent, x, y, w, h, title) => {
    const g = el("g", {}, parent);
    el("rect", { x, y, width: w, height: h, rx: 14, fill: COLORS.panel, stroke: COLORS.panelLine, "stroke-width": 1 }, g);
    el("text", { x: x + w - 14, y: y + 22, "text-anchor": "end", "font-size": 14, fill: COLORS.line }, g).textContent = title;
    return g;
  };

  // A tensor as a grid of cells (rows x cols), with its dimensions on the left and on top.
  // Arrows coming in from the left should enter below the middle, so as not to cross the label of the rows.
  const grid = (parent, { x, y, rows, cols, cell = 14, top = "", left = "" }) => {
    const g = el("g", {}, parent);
    const cells = [];
    for (let r = 0; r < rows; r++) {
      cells.push([]);
      for (let c = 0; c < cols; c++) {
        cells[r].push(el("rect", { x: x + c * cell, y: y + r * cell, width: cell, height: cell, fill: "#ffffff", stroke: COLORS.line, "stroke-width": 0.8 }, g));
      }
    }
    el("rect", { x, y, width: cols * cell, height: rows * cell, fill: "none", stroke: COLORS.line, "stroke-width": 1.4 }, g);
    if (top) tex(g, x + (cols * cell) / 2, y - 10, top, "middle");
    if (left) tex(g, x - 6, y + (rows * cell) / 2 + 5, left, "end");
    return { g, cells, x, y, w: cols * cell, h: rows * cell, rows, cols, cell };
  };

  // Write text into an SVG text element, "_x" or "_{xy}" becoming a subscript (fallback when MathJax is missing)
  const write = (t, text) => {
    const parts = text.split(/_(\{[^}]*\}|[A-Za-z0-9])/);
    parts.forEach((part, i) => {
      if (!part) return;
      const sub = i % 2 === 1;
      const span = el("tspan", sub ? { "baseline-shift": "sub", "font-size": "75%" } : {}, t);
      span.textContent = sub ? part.replace(/[{}]/g, "") : part;
    });
    return t;
  };

  // LaTeX rendered by MathJax as an SVG, its baseline at (x, y); without MathJax (or if it fails), a plain fallback
  const tex = (parent, x, y, latex, anchor = "middle", size = 14) => {
    let node = null;
    try { node = window.MathJax?.tex2svg?.(latex, { display: false }).querySelector("svg"); } catch (e) { node = null; }
    if (!node) {
      const plain = latex.replace(/\\(mathbf|boldsymbol|mathrm|text)\{([^}]*)\}/g, "$2").replace(/\\cdot/g, "·").replace(/\\times/g, "×").replace(/\\[a-zA-Z]+/g, "").replace(/[{}]/g, "");
      return write(el("text", { x, y, "text-anchor": anchor, "font-size": size, "font-style": "italic", "font-family": "Georgia, serif", fill: COLORS.line }, parent), plain);
    }
    const ex = size * 0.44, w = parseFloat(node.getAttribute("width")) * ex, h = parseFloat(node.getAttribute("height")) * ex;
    const va = parseFloat((node.style.verticalAlign || "0").replace("ex", "")) * ex;
    node.setAttribute("width", w);
    node.setAttribute("height", h);
    node.setAttribute("x", x - (anchor === "middle" ? w / 2 : anchor === "end" ? w : 0));
    node.setAttribute("y", y - h - va);
    node.setAttribute("style", `color: ${COLORS.line}; overflow: visible`);
    parent.append(node);
    node.dataset.width = w;
    return node;
  };

  // A line mixing words and $…$ LaTeX, its baseline at (x, y), aligned as a whole
  const rich = (parent, x, y, line, { anchor = "middle", size = 13.5, weight = 400, fill = COLORS.line } = {}) => {
    const g = el("g", {}, parent);
    let cursor = 0;
    line.split("$").forEach((part, i) => {
      if (!part) return;
      if (i % 2) {
        const node = tex(g, cursor, y, part, "start", size + 0.5);
        cursor += Number(node.dataset.width || node.getComputedTextLength?.() || 0);
      } else {
        const t = el("text", { x: cursor, y, "font-size": size, "font-weight": weight, fill, style: "white-space: pre" }, g);
        t.textContent = part;
        cursor += t.getComputedTextLength();
      }
    });
    g.setAttribute("transform", `translate(${x - (anchor === "middle" ? cursor / 2 : anchor === "end" ? cursor : 0)}, 0)`);
    return g;
  };

  // A name and an equation under a tensor, one line each; "$…$" parts are LaTeX
  const label = (parent, x, y, lines) => lines.forEach((line, i) => rich(parent, x, y + i * 19, line));

  // An arrow through the given points, turning at right angles: [[x0, y0], [x1, y1], ...]
  const arrow = (parent, points, head = true) =>
    el("polyline", { points: points.map((p) => p.join(",")).join(" "), fill: "none", stroke: COLORS.line, "stroke-width": 1.4, ...(head ? { "marker-end": "url(#arrow)" } : {}) }, parent);

  // Legend of the dimensions: a title, a thin rule, then the items one after the other over the whole width,
  // going to the next line only when the line is full. Each item is [LaTeX symbol, words] or a line with $…$
  const legend = (parent, x, y, items, { title = "Legend", width = 640 } = {}) => {
    const g = el("g", {}, parent);
    el("text", { x, y, "font-size": 12.5, "font-weight": 600, fill: COLORS.line }, g).textContent = title;
    el("line", { x1: x, x2: x + width, y1: y + 9, y2: y + 9, stroke: COLORS.line, "stroke-opacity": 0.3 }, g);
    let cx = x, row = 0;
    items.forEach((item) => {
      const line = typeof item === "string" ? item : `$${item[0]}$: ${item[1]}`;
      const node = rich(g, 0, y + 30, line, { anchor: "start", size: 12.5, fill: "#444" });
      const w = node.getBBox().width;
      if (cx > x && cx + w > x + width) { cx = x; row += 1; }
      node.setAttribute("transform", `translate(${cx}, ${row * 20})`);
      cx += w + 28;
    });
    return g;
  };

  // White to brown, as the attention weights of the book (t in [0, 1])
  const heat = (t) => {
    const a = [255, 245, 235], b = [127, 39, 4];
    return `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * Math.min(Math.max(t, 0), 1))).join(",")})`;
  };

  // Run a drawing once MathJax is ready, so that its labels are typeset; without MathJax after 5 s, draw anyway
  const ready = (draw) => {
    let tries = 0;
    const wait = setInterval(() => {
      const promise = window.MathJax?.startup?.promise;
      if (promise || ++tries > 100) { clearInterval(wait); (promise || Promise.resolve()).then(draw); }
    }, 50);
  };

  // Show a group fully, or faded when it is not part of the current step
  const show = (g, on) => g.setAttribute("opacity", on ? 1 : COLORS.faded);

  // Step-by-step player: a progress bar over the steps, previous and next, two pauses (one for going through the
  // steps, one for the animation inside the current step) and a restart, which plays everything from the first step. Autoplay unless the reader prefers reduced motion.
  // steps: [{ text: "<span lang='fr'>…</span><span lang='en'>…</span>", draw: (tick) => {} }]; draw is called
  // with tick = 0, 1, 2, … every `beat` ms while the inner animation plays; a step lasts `perStep` beats.
  const player = (container, steps, { beat = 900, perStep = 6 } = {}) => {
    // Icons drawn in SVG (fonts on phones lack some media symbols), in the colour of the button
    const icon = (d) => `<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="${d}" fill="currentColor"/></svg>`;
    const ICONS = {
      prev: icon("M10.5 3 5 8l5.5 5 1-1.1L7.2 8l4.3-3.9z"),
      next: icon("M5.5 3 11 8l-5.5 5-1-1.1L8.8 8 4.5 4.1z"),
      play: icon("M5 3v10l8-5z"),
      pause: icon("M4 3h3v10H4zm5 0h3v10H9z"),
      steps: icon("M2 3v10l6-5zm6 0v10l6-5z"),
      restart: icon("M8 2a6 6 0 1 0 6 6h-1.6A4.4 4.4 0 1 1 8 3.6V6l3.5-3L8 0z"),
    };
    container.classList.add("anim");
    const bar = document.createElement("div");
    bar.className = "player";
    bar.innerHTML = `<button type="button" data-a="prev" title="Étape précédente / Previous step">${ICONS.prev}</button>`
      + `<input type="range" min="0" max="${steps.length - 1}" step="1" value="0" aria-label="Step">`
      + `<button type="button" data-a="next" title="Étape suivante / Next step">${ICONS.next}</button><span class="count"></span>`
      + `<button type="button" data-a="steps" title="Défilement des étapes / Go through the steps">${ICONS.steps}</button>`
      + '<button type="button" data-a="anim" title="Animation de l\'étape / Animation of the step"></button>'
      + `<button type="button" data-a="reset" title="Recommencer / Restart">${ICONS.restart}</button>`;
    const caption = document.createElement("p");
    caption.className = "step-text";
    // Controls and the text of the step above the drawing, so that the caption of the figure follows it directly
    container.prepend(bar, caption);
    const range = bar.querySelector("input");
    const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
    let step = 0, tick = 0, elapsed = 0, stepsOn = !reduce, animOn = !reduce;
    const render = () => {
      steps[step].draw(tick);
      caption.innerHTML = steps[step].text;
      window.MathJax?.typesetPromise?.([caption]);
      range.value = step;
      bar.querySelector(".count").textContent = `${step + 1} / ${steps.length}`;
      const b1 = bar.querySelector('[data-a="steps"]'), b2 = bar.querySelector('[data-a="anim"]');
      b2.innerHTML = animOn ? ICONS.pause : ICONS.play;
      b1.setAttribute("aria-pressed", String(stepsOn));
      b2.setAttribute("aria-pressed", String(animOn));
    };
    const go = (i) => { step = (i + steps.length) % steps.length; tick = 0; elapsed = 0; render(); };
    setInterval(() => {
      if (animOn) { tick += 1; steps[step].draw(tick); }
      if (stepsOn && ++elapsed >= perStep) go(step + 1);
    }, beat);
    range.addEventListener("input", () => { stepsOn = false; go(Number(range.value)); });
    bar.addEventListener("click", (e) => {
      const a = e.target.closest("button")?.dataset.a;
      if (a === "prev") { stepsOn = false; go(step - 1); }
      if (a === "next") { stepsOn = false; go(step + 1); }
      if (a === "steps") { stepsOn = !stepsOn; elapsed = 0; render(); }
      if (a === "anim") { animOn = !animOn; render(); }
      if (a === "reset") { stepsOn = true; animOn = true; go(0); }
    });
    go(0);
    return { go };
  };

  return { el, svg, panel, grid, tex, rich, label, legend, arrow, heat, show, ready, player, COLORS };
})();
