r"""Common matplotlib style and colours of the figures (import or copy into the analysis script)."""

import matplotlib.pyplot as plt

# fmt: off
#
# ----- Colours: colourblind-safe groups, then train / validation / test
#
GROUPS = ["#0072B2", "#E69F00", "#009E73", "#D55E00"]
SPLITS = {"train": "#2a78d6", "validation": "#eb6834", "test": "#1baf7a"}
MUTED  = "#9a9a9a"
# fmt: on

plt.rcParams.update({
    "font.size": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e5e5e5",
    "grid.linewidth": 0.5,
    "figure.dpi": 110,
    "figure.constrained_layout.use": True,
})
