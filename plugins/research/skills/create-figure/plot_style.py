r"""Common matplotlib style and colours of the figures (import or copy into the analysis script)."""

import matplotlib.pyplot as plt

# fmt: off
#
# ----- Colours: colourblind-safe groups (blue, amber, green, vermilion: the same names as the colour classes of the
#       report captions), the train / validation / test splits in that order, and grey for a reference
#
GROUPS = ["#0072B2", "#E69F00", "#009E73", "#D55E00"]
SPLITS = {"train": GROUPS[0], "validation": GROUPS[1], "test": GROUPS[2]}
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
    "savefig.dpi": 256,              # every saved figure: PNG at 256 dpi, sharp on Retina screens
    "savefig.format": "png",
    "figure.constrained_layout.use": True,
    "figure.constrained_layout.h_pad": 0.08,
    "figure.constrained_layout.w_pad": 0.08,
    "figure.constrained_layout.hspace": 0.06,
    "figure.constrained_layout.wspace": 0.04,
})
