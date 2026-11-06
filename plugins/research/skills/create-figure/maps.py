r"""Map helpers following the rules of the create-figure skill (§ 7): import or copy into the analysis script.

`color_limits` only needs numpy; the other helpers need cartopy, imported when first called so that a missing
cartopy gives a clear error instead of breaking the import of this module.
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Rectangle
from matplotlib.ticker import FormatStrFormatter


def _cartopy():
    r"""Import cartopy, with a clear error when it is missing.

    Returns:
        ccrs     : The module cartopy.crs.
        cfeature : The module cartopy.feature.
    """
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
    except ImportError as error:
        raise ImportError(
            "maps.py needs cartopy: ask Victor before adding it to the environment (pyproject.toml), "
            "then install it, e.g. `uv add cartopy` or `pip install cartopy`."
        ) from error
    return ccrs, cfeature


def color_limits(field: np.ndarray, extreme: bool = False, diverging: bool = False) -> tuple[float, float]:
    r"""Compute the limits of a colormap from the 2% and 98% quantiles of a field.

    Arguments:
        field     : Field or stack of panels sharing their limits, NaN on land.
        extreme   : Whether the field shows an extreme event (full range instead of the quantiles).
        diverging : Whether the field is signed (limits centred on zero).

    Returns:
        vmin : Lower limit of the colormap.
        vmax : Upper limit of the colormap.
    """
    vmin, vmax = np.nanquantile(field, [0, 1] if extreme else [0.02, 0.98])
    if diverging:
        vmax = max(abs(vmin), abs(vmax))
        vmin = -vmax
    return float(vmin), float(vmax)


def add_geography(ax: plt.Axes, scale: str = "50m") -> None:
    r"""Add the contours and the longitude and latitude axes to a map.

    Arguments:
        ax    : Map axis, with the projection PlateCarree.
        scale : Resolution of Natural Earth ("10m", "50m" or "110m").
    """
    _, cfeature = _cartopy()

    for feature in (cfeature.COASTLINE, cfeature.BORDERS, cfeature.LAKES):
        ax.add_feature(feature.with_scale(scale), facecolor="none", edgecolor="black", linewidth=0.4)

    gridlines = ax.gridlines(draw_labels=True, linewidth=0)
    gridlines.top_labels = gridlines.right_labels = False
    gridlines.xformatter = gridlines.yformatter = FormatStrFormatter("%g")

    fraction = dict(xycoords="axes fraction", textcoords="offset points", va="center")
    ax.annotate(r"Longitude [$^\circ$E]", (0.5, 0), (0, -30), ha="center", **fraction)
    ax.annotate(r"Latitude [$^\circ$N]", (0, 0.5), (-35, 0), ha="right", rotation=90, **fraction)


def plot_map(
    ax: plt.Axes,
    lon: np.ndarray,
    lat: np.ndarray,
    field: np.ndarray,
    label: str,
    vmin: float,
    vmax: float,
    cmap: str = "viridis",
) -> None:
    r"""Plot a field on a map, with a colorbar of the height of the axis.

    Arguments:
        ax    : Map axis, with the projection PlateCarree.
        lon   : Longitudes (X) [°E].
        lat   : Latitudes (Y) [°N].
        field : Field to plot, NaN on land (Y, X).
        label : Label of the colorbar, with the unit in brackets.
        vmin  : Lower limit of the colormap.
        vmax  : Upper limit of the colormap.
        cmap  : Name of the colormap.
    """
    ccrs, _ = _cartopy()

    image = ax.pcolormesh(lon, lat, field, cmap=cmap, vmin=vmin, vmax=vmax, transform=ccrs.PlateCarree())
    add_geography(ax)

    # Bounds relative to the axis: same height for any projection or aspect ratio, arrows included.
    clipped = (np.nanmin(field) < vmin, np.nanmax(field) > vmax)
    extend = {(0, 0): "neither", (1, 0): "min", (0, 1): "max", (1, 1): "both"}[tuple(map(int, clipped))]
    ax.figure.colorbar(image, cax=ax.inset_axes([1.02, 0, 0.03, 1]), label=label, extend=extend)


def plot_zones(ax: plt.Axes, extent: list[float], zones: dict[str, list[float]]) -> None:
    r"""Plot the map of all the zones named in a report.

    Arguments:
        ax     : Map axis, with the projection PlateCarree.
        extent : Limits of the map [°E, °E, °N, °N].
        zones  : Name and limits of each zone [°E, °E, °N, °N].
    """
    ccrs, _ = _cartopy()

    crs = ccrs.PlateCarree()
    ax.set_extent(extent, crs=crs)
    add_geography(ax)

    for name, (west, east, south, north) in zones.items():
        ax.add_patch(Rectangle((west, south), east - west, north - south, fill=False, linewidth=1.5, transform=crs))
        ax.text((west + east) / 2, north, name, ha="center", va="bottom", weight="bold", transform=crs)
