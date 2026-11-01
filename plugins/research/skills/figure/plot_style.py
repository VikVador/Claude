r"""Common matplotlib style and colours of the figures (import or copy into the analysis script)."""

import matplotlib.pyplot as plt

# fmt: off
#
# ----- Colours: colourblind-safe groups, then train / validation / test
#
GROUPS = ["#0072B2", "#E69F00", "#009E73", "#D55E00"]  # blue, amber, green, vermilion: same names in the report
SPLITS = {"train": "#2a78d6", "validation": "#eb6834", "test": "#1baf7a"}
MUTED  = "#9a9a9a"
# fmt: on

# One size for titles, labels and legends, a little smaller for the ticks, room between ticks and labels, and
# mathematics in Computer Modern, as LaTeX in the reports
plt.rcParams.update({
    "font.size": 10,
    "mathtext.fontset": "cm",
    "axes.titlesize": 10.5,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.titlepad": 8,
    "axes.labelpad": 8,
    "xtick.major.pad": 4,
    "ytick.major.pad": 4,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.dpi": 110,
    "figure.constrained_layout.use": True,
    "figure.constrained_layout.h_pad": 0.08,
    "figure.constrained_layout.w_pad": 0.08,
    "figure.constrained_layout.hspace": 0.06,
    "figure.constrained_layout.wspace": 0.04,
})
