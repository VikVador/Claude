# Examples of figures

Figures of the lecture this skill is built on: Gilles Louppe, *Foundations of Data Science*, lecture 3, Visualization
(University of Liège), https://glouppe.github.io/dats0001-foundations-of-data-science/?p=lecture3.md. Each image keeps
the credit of its original author, given below. Only the figures that show good practice are kept; they are here to learn from, not to copy.

**How to use**: when choosing a plot or checking one, find the matching topic below and open its image(s) with the
Read tool. The slide text and notes say what each figure does well.

### Two kinds of plots

Files: `examples/exploratory-explanatory.png`

Slide:

- Exploratory: for yourself, quickly and in numbers, to see (Lecture 2).
- Explanatory: for others, few and polished, to carry one message.

Notes:
The building blocks are the same, the standards are not. The same plots come back in Lecture 7, on what a model gets wrong.

Credit: Gilles Louppe, DATS0001 lecture 3

### Start from the message

Files: `examples/four-questions.png`

Slide: Decide first what the plot must show: a comparison, a distribution, a correlation or an evolution.

Notes:
For subsets, either distinguish them within one panel, or juxtapose panels sharing identical scales.

Credit: [Doumont](https://www.principiae.be/X0100.php), Trees, maps, and theorems, 2009.

### Anatomy of a plot

Files: `examples/anatomy.png`

Slide: data → marks → channels → scales → coordinates → guides

Notes:
The rest of the lecture takes these pieces in order.

Credit: The grammar of graphics: Wilkinson, 1999; implemented in ggplot2, Vega-Lite, Altair and seaborn objects.

### Visual cues

Files: `examples/marks.png`

Slide: Visual cues are elements of a visualization that encode data. They are expressed as marks and channels:

- A mark is a geometric primitive such as points, lines, or areas.
- A channel is an attribute of a mark that can be used to encode data, such as position, size, shape, or color.

Credit: T. Munzner, "Visualization Analysis and Design", 2014.

### Visual cues

Files: `examples/channels.png`

Slide: Visual channels control the appearance of marks.

Credit: T. Munzner, "Visualization Analysis and Design", 2014.

### Visual cues

Files: `examples/encoding-examples.png`

Slide: (a) Bar charts encode data using line marks, controlled by a vertical position channel (height) and a horizontal position channel (category). (b) Scatterplots encode data using point marks, controlled by two position channels (x and y). (c) A third variable can be encoded using a color channel. (d) A fourth variable can be encoded using a size channel (area of the point).

Credit: Gilles Louppe, DATS0001 lecture 3

### Overplotting

Files: `examples/overplotting.png`

Slide: Flipper lengths are whole millimetres, body masses multiples of 25 g, so identical readings stack. Transparency, jitter or binning give the density back.

Credit: Gilles Louppe, DATS0001 lecture 3

### Perceptual hierarchy

Files: `examples/ladder.png`

Slide: Not all channels are read equally well.

Credit: T. Munzner, "Visualization Analysis and Design", 2014.

### Perceptual hierarchy

Files: `examples/cleveland.png`

Slide: Cleveland and McGill (1984) conducted experiments to evaluate the accuracy of visual channels for encoding quantitative data.

Notes:
In each task, two marks are highlighted, and participants estimate what percentage the smaller is of the larger.
- T1 to T5 are the five bar-chart cases of Cleveland and McGill. T1 and T3 compare two bars on a common baseline, adjacent then apart; T2 compares the bottom segments of two stacked bars, still on the baseline; in T4 and T5 the segments sit inside stacked bars, off any common baseline, so the reader judges a length rather than a position.
- T6 compares two slices of a pie: angles.
- T7 compares two circles: areas.
- T8 compares two rectangles side by side, T9 two rectangles inside a treemap: areas again.

The horizontal axis is the log of the absolute error, so further right is worse, and the bars are 95% confidence intervals. The top panel is the original experiment (Cleveland and McGill, 1984); the bottom one is a replication with crowd workers on Mechanical Turk (Heer and Bostock, 2010), which adds T6 to T9 and finds the same order: positions on a common scale, then lengths, then angles, then areas.

Credit: T. Munzner, "Visualization Analysis and Design", 2014.

### Colors

Files: `examples/sphx_glr_colormaps_002.png`, `examples/sphx_glr_colormaps_004.png`, `examples/sphx_glr_colormaps_006.png`

Credit: [Choosing colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html).

### Colors

Files: `examples/sphx_glr_colormaps_001.png`

Slide: Perceptually uniform colormaps ensure that equal steps in data are perceived as equal steps in color.

Credit: [Choosing colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html).

### Colors

Files: `examples/popout.png`

Slide: Finally, colors can also be used to draw attention to specific elements in a visualization, such as highlighting important data points or trends. A single channel pops out at a glance; two channels at once must be searched.

Credit: Gilles Louppe, DATS0001 lecture 3

### Small multiples

Files: `examples/small-multiples.png`

Slide: Subsets can be told apart within one panel, by colour, or split into panels sharing their scales. Keeping the other points in grey gives each panel its reference.

Credit: Gilles Louppe, DATS0001 lecture 3

### Scales and transformations

Files: `examples/scale-log.png`

Slide: Showing data on a logarithmic scale can prevent large values from dominating the visualization and reveal patterns among smaller values. However, a logarithmic scale also hides absolute differences, cannot show zero or negative values, and is read as linear by an audience that does not expect it.

Credit: Data: `data/countries.csv`.

### Scales and transformations

Files: `examples/scale-quantile.png`

Slide: A quantile scale puts the same number of countries in each class; equal-width classes leave almost all of them in the lightest.

Notes:
One square per country, grouped by region and in alphabetical order within it, so that only the colour carries the GDP, as on a map.
The classes differ in width, from 500 to 1600 dollars for the first and from 18600 to 55100 for the last, so a quantile scale says who is ahead of whom, not by how much. It is the usual choice for the colours of a choropleth map.

Credit: Data: `data/countries.csv`, GDP per capita.

### Binning is a choice

Files: `examples/binning.png`

Slide: The same 342 body masses. Too few bins hide the second group, too many show noise as structure.

Credit: Gilles Louppe, DATS0001 lecture 3

### Guides

Files: `examples/guides.png`

Slide: A legend costs a lookup for every group. Labelling them in place, and annotating the one thing the reader should notice, costs nothing.

Credit: Gilles Louppe, DATS0001 lecture 3

### Show the uncertainty

Files: `examples/uncertainty.png`

Slide:

- Left: one bar per species, and the birds are gone.
- Middle: every bird, with the mean and its 95% interval.
- Right: the same Adelie mean, with three different error bars.

The standard deviation is the spread of the birds; the standard error is the uncertainty on the mean.

Notes:
The left bars are one standard error, and the figure does not say so: that is the fault it illustrates. The middle bars are 95% intervals for the mean. Both look tiny because, with about 150 birds per species, the mean is known to within a few dozen grams, while the birds themselves spread over more than a kilogram.

**Always say in the caption what the error bars show.**

Credit: Gilles Louppe, DATS0001 lecture 3

### Show the uncertainty

Files: `examples/spaghetti-ensemble.png`

Slide: Ten forecasts of the same contour, three days ahead. Too many lines on purpose: the message is the spread.

Notes:
The annotation does the rest of the work, circling where the forecasts disagree.
From Lecture 7 on, the same holds for what a model predicts.

Credit: NOAA/NCEP [Environmental Modeling Center](https://www.emc.ncep.noaa.gov/), 500 hPa ensemble forecast, 19 November 2001 (public domain).

### Lengths rather than angles

Files: `examples/bar-chart.png`

Slide: Same data! Lengths and positions are easier to compare than angles and areas.

Notes:
A pie is readable for two or three slices adding up to a whole. Beyond that, it asks the reader to compare angles.

Credit: Gilles Louppe, DATS0001 lecture 3

### Bars start at zero

Files: `examples/colorado-real.png`

Credit: John Muyskens, [Most of Trump's charts skew the data](https://www.washingtonpost.com/graphics/politics/2016-election/trump-charts/), The Washington Post, 2016.

### Visualize the rawest data

Files: `examples/datasaurus.png`

Slide: Summary statistics can be misleading. Always visualize the rawest data !

Credit: [Matejka & Fitzmaurice](https://www.research.autodesk.com/publications/same-stats-different-graphs/), 2017.
