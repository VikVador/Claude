---
name: figure
description: "Use before drawing or fixing any figure meant to carry a scientific message (plots, charts, maps of results, data or diagnostics), for a report, a slide or on its own, in any project. Gives the rules to choose the plot, the colours, the scales, the captions, the uncertainty and the maps, the style of plot_style.py, the cartopy map helpers of maps.py, and a checklist. Not for diagrams of a mechanism (diagram skill)."
---

```text
     ┌───────┐
     │ ◉   ◉ │       C   L   A   U   D   E
     │   ▿   │
     └─┬───┬─┘       Figures: how to draw a figure that carries
     ┌─┴───┴─┐       a scientific message.
     │ ▓▓▓▓▓ │
     └─┘   └─┘
```

# FIGURE

Every figure carries one message, that the reader gets at a glance and cannot misread. Read this file before drawing
any figure, for a report, a slide or on its own, and before fixing an existing one.

**Last checked: 2026-10-30** (every link of § 10 was opened and verified on that day).

| File            | Use                                                                                      | When                                  |
| --------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| `plot_style.py` | **Run** by importing it (§ 1): the style, and the colours `GROUPS`, `SPLITS`, `MUTED`    | every figure                          |
| `maps.py`       | **Run** by importing it (§ 7): `color_limits`, `add_geography`, `plot_map`, `plot_zones` | every map                             |
| `examples.md`   | **Read**, then open the matching images of `examples/` with the Read tool                | when choosing or checking a plot type |

Related: the `report` skill for the structure of a report, the `presentation` skill for where a figure goes on a
slide, the `diagram` skill for diagrams and animations that explain a mechanism.

**Contents**

0. In short
1. Work order
2. Figures in a report or on a slide
3. Choosing the plot
4. Encoding and colours
5. Scales
6. Guides, captions and uncertainty
7. Maps
8. Anti-patterns
9. Checklist
10. Sources

---

## 0. IN SHORT

1. **I like figures**: when a result can be shown, show it. The text explains the figure, not the other way around.
2. **Start from the message**: a comparison, a distribution, a correlation or an evolution, said in one sentence (§ 3).
3. **Do not let the reader misread**: position before colour, no rainbow, no cut bars, no 3D, uncertainty shown.
4. **Geographic data**: first one map of every zone named in the text, then every map drawn with `maps.py` (§ 7).
5. **Look before delivering**: open the saved PNG with the Read tool and run the checklist (§ 9).
6. **Ask me first** before adding `cartopy` or `cmocean` to an environment.

---

## 1. WORK ORDER

1. **Say the message in one sentence**: it opens the caption (report), or it is the caption or the box (slide).
2. **Pick the plot** (§ 3); when unsure, open the matching example of `examples.md`.
3. **Import `plot_style`** (and `maps.py` for a map) from `<skill folder>`, the "Base directory for this skill" shown
   when the skill loads:
   ```python
   import sys
   sys.path.insert(0, "<skill folder>")
   from plot_style import GROUPS, SPLITS, MUTED  # sets the style on import
   ```
4. **Draw** following § 4 to § 7, at the size of § 2.
5. **Save** as PNG at `dpi=110` or more, then **open the PNG with the Read tool and look at it**: overlapping or cut
   text, unreadable ticks, a colorbar of the wrong size, a legend on the data.
6. **Run the checklist** (§ 9), fix, save and look again, until every box is ticked.

To fix an existing figure, start at step 5: look at it, run the checklist, then go back to the step that failed.

---

## 2. FIGURES IN A REPORT OR ON A SLIDE

| Rule                    | In practice                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| Figures first           | every result comes with a figure; prefer a figure to a paragraph of numbers                 |
| One figure, one message | no title on the figure: the caption states the finding (on a result slide, the caption or the box) |
| Explanatory, not a dump | as many figures as there are messages; an exploratory sweep stays out of the report         |
| Rawest data first       | show fields and samples before their summaries: the same statistics can hide anything       |
| All the data            | no subset of runs, dates or zones without saying so: the pattern may be in what is cut      |
| Same choices everywhere | one variable, model or zone keeps the same colour, name and order in the whole report       |
| Table or figure         | a table for exact numbers, a heatmap or lines for a pattern, never bars with printed values |
| Metrics                 | from the project's metrics library (e.g. `albus`) rather than from a new implementation     |
| Size in a report        | the text column (960 px): `figsize` about 10 to 11 inches wide, PNG at `dpi=110` or more    |
| Size on a slide         | a result slide (16:9, 1280×720) leaves the figure about **1080 × 350 px** above a one-line caption and box: draw it for that room, `figsize` about 9.8 × 3.2 inches at `dpi=110` (wide, about 3:1), font sizes kept; one figure per message, never a multi-row figure shrunk to fit |

---

## 3. CHOOSING THE PLOT

| Message      | Plot                                                            | Example                           |
| ------------ | --------------------------------------------------------------- | --------------------------------- |
| Comparison   | bars starting at zero, or dots                                  | skill of several models           |
| Distribution | all the points along an axis, or a histogram / box plot if many | sea surface temperature at a site |
| Correlation  | a scatter plot, a matrix of scatter plots above two variables   | predicted against true oxygen     |
| Evolution    | a line against time or another ordered variable                 | CRPS against the lead time        |

- **Subsets**: tell them apart within one panel, or use small multiples **sharing their scales**. Keeping the other
  points in grey gives each panel its reference.
- **Overplotting**: use transparency, jitter or binning to give the density back.
- **Coordinates**: Cartesian by default. Polar only for cyclic data (seasons), as it distorts lengths.

---

## 4. ENCODING AND COLOURS

Channels from the most to the least accurately read: **position on a common scale > position on unaligned scales >
length > angle > area > depth > luminance, saturation > curvature, volume.** So a map, read through colour, shows
**where**. To compare **how much**, add a line, a transect or a profile.

| Data                         | Colormap                                                                           |
| ---------------------------- | ---------------------------------------------------------------------------------- |
| Ordered                      | sequential and perceptually uniform: `viridis`, `cividis`                          |
| Ordered, meaningful midpoint | diverging, centred on the midpoint: `RdBu_r`, `cmo.balance`                        |
| Unordered groups             | few colourblind-safe colours, `GROUPS`: `#0072B2`, `#E69F00`, `#009E73`, `#D55E00` |
| Ocean fields                 | `cmo.thermal`, `cmo.haline`, `cmo.algae`, `cmo.speed`: temperature, salinity, chlorophyll, current speed |

- **Never `jet` or a rainbow**: it invents edges and bands that are not in the data.
- A signed quantity (anomaly, bias) is diverging. A positive one (RMSE, CRPS, spread) is sequential.
- An ordered quantity (lead time, noise level) gets a sequential colormap, not categorical colours.
- **Colour never carries alone** what the reader must not miss (1 in 12 men has a colour vision deficiency):
  repeat it with position, shape or a label.
- Colour can draw attention: everything in grey (`MUTED`), the one thing to notice in colour.

---

## 5. SCALES

| Scale       | When                                 | Beware                                                         |
| ----------- | ------------------------------------ | -------------------------------------------------------------- |
| Linear      | by default                           | large values can dwarf the small ones                          |
| Logarithmic | several orders of magnitude, spectra | hides absolute differences, no zero nor negative value; the ticks show it, never "(log scale)" in a label |
| Quantile    | skewed data, equal-count classes     | says who is ahead, not by how much (not the limits of § 7)     |

- **Binning is a choice**: too few bins hide a group, too many show noise as structure. Try several.
- **A value read against a limit** (memory against the size of a GPU, a threshold): linear scale, with a line
  per limit, so the distance to the limit reads directly.
- **Bars start at zero**, as they encode a length. Dots and lines encode a position and can show a narrow range.
- No misleading aspect ratio.

---

## 6. GUIDES, CAPTIONS AND UNCERTAINTY

- **Label in place** rather than with a legend, and **annotate** the one thing the reader should notice.
- A legend, if needed, never covers data. A colorbar or legend shared by panels is given once.
- **Axes**: quantity and unit in `[]`, with maths in LaTeX, on every figure, e.g.
  `r"Temperature [$^\circ\mathrm{C}$]"`, `r"Zonal current [$\mathrm{m\,s^{-1}}$]"`,
  `r"Wind stress [$\mathrm{N\,m^{-2}}$]"`, `r"Oxygen [$\mathrm{mmol\,m^{-3}}$]"`, `r"Sea surface height [$\mathrm{m}$]"`.
  These are examples: take the true unit from the metadata of the dataset.
- **All mathematics in LaTeX** (`$…$`), rendered in Computer Modern by `plot_style.py`, so that figures, text and
  diagrams look the same: symbols, formulas and units, e.g. `r"$\sigma/\tau$"`.
- **A quantity without unit** (a ratio, a fraction, a normalised loss) gets `[$-$]`: `r"Fraction of the schedule [$-$]"`.
- **Spell out** quantities and variables in labels and panel titles rather than acronyms:
  `r"Geometric embedding loss [$-$]"`, not `GME`; `Sea surface temperature`, not `SST`.
- **Panels of the same quantity share their axes** (`sharex`, `sharey`), labelled only on the outer panels (x on the
  bottom row, y on the first column): less repeated text, and the panels are seen aligned. Runs of different lengths
  share a common x scale (e.g. a fraction of the schedule) when it does not squeeze the information.
- **Caption**: first what the figure shows, in a few words (in semibold in a report); then how to read it: x axis,
  y axis, what each curve or colour is; then period, zone, depth, number of samples or members, colour limits.
  On a slide, one short caption: the finding, and what to look at.
- **Show the uncertainty**: a mean alone hides the data. Show the points with the mean and its interval.
- **Always say what the error bars show**: the standard deviation is the spread of the data, the standard error the
  uncertainty on the mean. Print which one.
- **Ensembles**: show the spread. Many lines are fine when the spread is the message (spaghetti plot).
- Remove what no one reads: background, top and right frames, and **no grid** unless asked for.
- **Let it breathe**: one font size for titles, labels and legends (ticks one point smaller), space between ticks
  and axis labels and between panels. `plot_style.py` sets all of this.
- **Text of figures in English**, made once, even in a French report.

---

## 7. MAPS

These are my own rules: they apply to **every figure showing a geographic zone**.

### The map of the zones

When a report works with geographic data, **one single figure** shows **all the zones named in the text**, before they
are used. Each zone is outlined and labelled in place, with the name used in the text. A new zone goes on this figure,
not on a second one.

### Each map

| Element  | Rule                                                                                       |
| -------- | ------------------------------------------------------------------------------------------ |
| Axes     | `Longitude [°E]`, `Latitude [°N]`                                                          |
| Units    | in `[]`, with maths in LaTeX (§ 6)                                                         |
| Colorbar | **exactly the size of the axis** it sits on: the height on the side, the width below       |
| Limits   | `vmin` and `vmax` are the **2% and 98% quantiles**, to keep contrast                       |
| Extreme  | **except** when showing an extreme event: then the full range, or the limits would hide it |
| Contours | thin black lines for the coasts, countries and lakes, to locate the plot                   |

And to stay honest with these limits:

- Compute them **ignoring the land** (`nanquantile`) and say them in the caption.
- The arrows at the ends of the colorbar show that values are clipped.
- Panels to compare **share their limits**, computed on all the panels, and a single colorbar spanning them.
- A signed field stays centred on zero: `vmax = max(|q2|, |q98|)`, `vmin = -vmax`.

### With `maps.py`

`color_limits`, `plot_map` and `plot_zones` apply these rules; `add_geography` adds the contours and the axes. Always
create the figure with `constrained_layout=True` (`plot_style.py` sets it) and the axis with
`projection=ccrs.PlateCarree()`.

```python
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from maps import color_limits, plot_map, plot_zones  # after the sys.path line above

on_map = dict(subplot_kw=dict(projection=ccrs.PlateCarree()))
fig, ax = plt.subplots(figsize=(10.5, 5), **on_map)
plot_zones(ax, extent=[-20, 40, 30, 70], zones={"North Sea": [-4, 9, 51, 61]})  # once, at the start
fig, ax = plt.subplots(figsize=(10.5, 5), **on_map)
vmin, vmax = color_limits(sst)  # extreme=True for an extreme event, diverging=True for a signed field
plot_map(ax, lon, lat, sst, r"Sea surface temperature [$^\circ\mathrm{C}$]", vmin, vmax, cmap="cividis")
fig.savefig("sst.png", dpi=110)
```

- `cartopy` (and `cmocean`) missing from the environment: ask me before adding them to `pyproject.toml` and
  installing them (on a cluster, follow its skill).
- `cartopy` downloads the contours of Natural Earth on first use: if a compute node has no internet access, run it once
  on a login node.

---

## 8. ANTI-PATTERNS

| Do not                          | Because                                              | Instead                      |
| ------------------------------- | ---------------------------------------------------- | ---------------------------- |
| Pie chart                       | angles are hard to compare                           | bars, or two or three slices |
| 3D                              | it distorts perception, and adds nothing             | position, then colour        |
| Cut a bar from zero             | a bar encodes a length: the cut exaggerates          | bars from zero, or dots      |
| Channels out of scale with data | the drawn difference must be the true one            | channel proportional to data |
| Only summary statistics         | identical statistics can hide any shape (Datasaurus) | plot the rawest data         |
| Plot only a subset              | Challenger: the pattern was in the flights left out  | plot everything              |
| Publish an exploratory sweep    | 72 panels and no message                             | one question, one plot       |

---

## 9. CHECKLIST

- [ ] Is the message said in one sentence, by the caption (or the box of a slide), with no title on the figure?
- [ ] Did you open the saved PNG with the Read tool? Is it at the size of § 2, with no text overlapping or cut, and no legend or label over the data?
- [ ] Is there a map of all the zones named in the text?
- [ ] Do all the axes and colorbars have a quantity and a unit in `[]`?
- [ ] Are the quantities spelled out, with `[$-$]` when they have no unit, and no "(log scale)" in a label?
- [ ] Is all the mathematics in LaTeX (`$…$`), and is the text of the figure in English?
- [ ] Do panels of the same quantity share their axes, labelled only on the outer panels? Is there no grid?
- [ ] Is each colorbar exactly the size of its axis?
- [ ] Are the limits the 2% and 98% quantiles, or the full range for an extreme event? Does the caption say so?
- [ ] Do the panels to compare share their scales?
- [ ] Is the colormap perceptually uniform, centred if the field is signed, and readable without colour vision?
- [ ] Is the uncertainty shown, and is it said what the error bars are?
- [ ] Is anything left out of the data? Is it said?

---

## 10. SOURCES

| Source                                  | Link                                                                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------- |
| Gilles Louppe, Lecture 3: Visualization | [dats0001](https://glouppe.github.io/dats0001-foundations-of-data-science/?p=lecture3.md#1) |
| Choosing colormaps in Matplotlib        | [matplotlib.org](https://matplotlib.org/stable/users/explain/colors/colormaps.html)         |
| Crameri et al. (2020), misuse of colour | [doi.org](https://doi.org/10.1038/s41467-020-19160-7)                                       |
| cmocean, colormaps for oceanography     | [matplotlib.org/cmocean](https://matplotlib.org/cmocean/)                                   |
| Cartopy                                 | [scitools.org.uk/cartopy](https://scitools.org.uk/cartopy/docs/latest/)                     |
