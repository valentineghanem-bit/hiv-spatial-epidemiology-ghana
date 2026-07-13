"""
Generate publication-ready Ghana manuscript maps.

This script regenerates Figures 1-4 with cartographic details required for a
journal-facing map: north arrow/bearing, scale bar, projection note, source
line, boundary caveat, and non-overlapping legends.
"""
from pathlib import Path

import geopandas as gpd
import matplotlib
from PIL import Image

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "outputs" / "data"
FIG_DIR = ROOT / "outputs" / "figures"
TIF_DIR = ROOT / "outputs" / "figures_cambridge"
GEOJSON = ROOT / "data" / "raw" / "Ghana_New_260_District.geojson"
CROSSWALK = ROOT / "docs" / "district_crosswalk_261_to_260.csv"
MASTER = DATA_DIR / "Ghana_HIV_Spatial_Analysis_MASTER.csv"

PROJECTED_CRS = "EPSG:32630"
SOURCE_BOUNDARY_NOTE = (
    "Source: Ghana DHS 2014/2022; Ghana Population & Housing Census 2021; "
    "Ghana Statistical Service 2023 boundaries."
)
GEOMETRY_NOTE = (
    "Map projection: WGS 84 / UTM zone 30N (EPSG:32630). "
    "Analytic frame: 261 census districts; mapped geometry: 260 unique polygons "
    "because Guan shares the Krachi East Municipal boundary."
)


plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "figure.titlesize": 16,
        "figure.titleweight": "bold",
        "savefig.dpi": 300,
    }
)


def load_map_frame() -> gpd.GeoDataFrame:
    master = pd.read_csv(MASTER)
    crosswalk = pd.read_csv(CROSSWALK)

    # Keep the same manually verified fixes used by the analytical pipeline.
    crosswalk.loc[
        crosswalk["master_sheet_district"] == "Awutu Senya West",
        ["geojson_district", "match_method"],
    ] = ["AWUTU SENYA", "manual_resolved_p2_audit"]
    crosswalk.loc[
        crosswalk["master_sheet_district"] == "Sagnarigu Municipal",
        ["geojson_district", "match_method"],
    ] = ["SAGNERIGU", "manual_resolved_p2_audit"]

    geo = gpd.read_file(GEOJSON)[["DISTRICT", "REGION", "geometry"]].copy()
    geo["DISTRICT"] = geo["DISTRICT"].str.strip()
    geo = geo.rename(columns={"REGION": "Boundary_Region"})

    non_gap = crosswalk[crosswalk["match_method"] != "structural_gap"].copy()
    gdf = geo.merge(
        non_gap[["master_sheet_district", "geojson_district"]],
        left_on="DISTRICT",
        right_on="geojson_district",
        how="left",
    )
    gdf = gdf.merge(master, left_on="master_sheet_district", right_on="District", how="left")
    if gdf["District"].isna().any() or len(gdf) != 260:
        missing = gdf.loc[gdf["District"].isna(), "DISTRICT"].tolist()
        raise ValueError(f"Boundary join failed. Missing districts: {missing[:10]}")

    guan = master.loc[master["District"] == "Guan"].iloc[0]
    krachi = master.loc[master["District"] == "Krachi East Municipal"].iloc[0]
    numeric_cols = master.select_dtypes(include="number").columns.tolist()
    idx = gdf.index[gdf["DISTRICT"] == "KRACHI EAST MUNICIPAL"]
    w1, w2 = float(krachi["Total_Pop"]), float(guan["Total_Pop"])
    for col in numeric_cols:
        if col == "Total_Pop":
            gdf.loc[idx, col] = w1 + w2
        else:
            gdf.loc[idx, col] = (krachi[col] * w1 + guan[col] * w2) / (w1 + w2)

    return gdf.set_geometry("geometry").set_crs("EPSG:4326").to_crs(PROJECTED_CRS)


def add_map_furniture(ax, gdf, scale_km=200, small=False):
    """Add north arrow, true-north bearing label, and alternating scale bar."""
    fontsize = 7 if small else 8
    ax.annotate(
        "",
        xy=(0.92, 0.91),
        xytext=(0.92, 0.80),
        xycoords="axes fraction",
        arrowprops=dict(facecolor="black", edgecolor="black", width=2.2, headwidth=9),
        zorder=20,
    )
    ax.text(
        0.92,
        0.94,
        "N\nBearing 0 deg",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=fontsize,
        fontweight="bold",
        bbox=dict(facecolor="white", edgecolor="0.75", alpha=0.86, boxstyle="round,pad=0.18"),
        zorder=21,
    )

    xmin, ymin, xmax, ymax = gdf.total_bounds
    width = xmax - xmin
    height = ymax - ymin
    seg_m = 100_000
    n_seg = max(1, int(scale_km / 100))
    total = seg_m * n_seg
    x0 = xmin + width * 0.055
    y0 = ymin - height * (0.075 if not small else 0.070)
    bar_h = height * (0.008 if not small else 0.006)
    for i in range(n_seg):
        rect = mpatches.Rectangle(
            (x0 + i * seg_m, y0),
            seg_m,
            bar_h,
            facecolor="black" if i % 2 == 0 else "white",
            edgecolor="black",
            linewidth=0.7,
            zorder=20,
        )
        ax.add_patch(rect)
    ax.plot([x0, x0 + total], [y0, y0], color="black", linewidth=0.7, zorder=21)
    ax.text(x0, y0 - height * 0.012, "0", ha="center", va="top", fontsize=fontsize, zorder=21)
    ax.text(
        x0 + total / 2,
        y0 - height * 0.012,
        f"{scale_km // 2}",
        ha="center",
        va="top",
        fontsize=fontsize,
        zorder=21,
    )
    ax.text(
        x0 + total,
        y0 - height * 0.012,
        f"{scale_km} km",
        ha="center",
        va="top",
        fontsize=fontsize,
        zorder=21,
    )


def style_map_axis(ax, gdf, pad=0.04, bottom_pad=0.14):
    xmin, ymin, xmax, ymax = gdf.total_bounds
    dx, dy = xmax - xmin, ymax - ymin
    ax.set_xlim(xmin - dx * pad, xmax + dx * pad)
    ax.set_ylim(ymin - dy * bottom_pad, ymax + dy * pad)
    ax.set_aspect("equal")
    ax.set_axis_off()


def add_footer(fig, text, y=0.025):
    fig.text(0.5, y, text, ha="center", va="bottom", fontsize=8.5, color="0.35")
    fig.text(0.5, y - 0.018, GEOMETRY_NOTE, ha="center", va="bottom", fontsize=8, color="0.45")


def save_figure(fig, stem):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TIF_DIR.mkdir(parents=True, exist_ok=True)
    png = FIG_DIR / f"{stem}.png"
    tif = TIF_DIR / f"{stem}.tif"
    fig.savefig(png, bbox_inches="tight", dpi=300)
    tmp = TIF_DIR / f"{stem}.__tmp.png"
    fig.savefig(tmp, bbox_inches="tight", dpi=300)
    with Image.open(tmp) as im:
        if im.mode in ("RGBA", "LA"):
            background = Image.new("RGB", im.size, "white")
            background.paste(im, mask=im.getchannel("A"))
            background.save(tif, dpi=(300, 300), compression="tiff_lzw")
        else:
            im.convert("RGB").save(tif, dpi=(300, 300), compression="tiff_lzw")
    tmp.unlink(missing_ok=True)
    plt.close(fig)
    print(f"Saved {png}")
    print(f"Saved {tif}")


def plot_numeric_panel(ax, gdf, column, title, cmap, legend_label):
    gdf.plot(
        column=column,
        ax=ax,
        cmap=cmap,
        edgecolor="white",
        linewidth=0.25,
        missing_kwds={"color": "#f0f0f0", "label": "Missing"},
    )
    style_map_axis(ax, gdf)
    add_map_furniture(ax, gdf, small=True)
    ax.set_title(title, pad=8)
    norm = Normalize(vmin=float(gdf[column].min()), vmax=float(gdf[column].max()))
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, shrink=0.58, fraction=0.045, pad=0.012)
    cbar.ax.set_ylabel(legend_label, rotation=90)
    cbar.outline.set_linewidth(0.7)


def figure_1(gdf):
    regions = sorted(gdf["Region"].unique())
    cmap = plt.get_cmap("tab20")
    colors = {region: cmap(i % 20) for i, region in enumerate(regions)}

    fig, ax = plt.subplots(figsize=(9.5, 13.5))
    for region in regions:
        gdf.loc[gdf["Region"] == region].plot(
            ax=ax,
            color=colors[region],
            edgecolor="white",
            linewidth=0.28,
        )
    style_map_axis(ax, gdf, pad=0.025)
    add_map_furniture(ax, gdf)
    ax.set_title("Figure 1. Ghana 261-district study area by 16 administrative regions", pad=16)

    handles = [mpatches.Patch(color=colors[r], label=r) for r in regions]
    ax.legend(
        handles=handles,
        title="Administrative region",
        loc="lower left",
        bbox_to_anchor=(1.01, 0.03),
        frameon=True,
        fontsize=8,
        title_fontsize=9,
    )
    ax.text(
        0.02,
        0.98,
        "Location: Ghana, West Africa\nBoundary layer: GSS 2023\nDisplayed units: 260 polygons",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox=dict(facecolor="white", edgecolor="0.72", alpha=0.88, boxstyle="round,pad=0.3"),
    )
    add_footer(fig, "Source: Ghana Statistical Service district boundary file; study analytic frame from linked DHS and Census datasets.")
    save_figure(fig, "fig1_study_area_map")


def figure_2(gdf):
    fig, axes = plt.subplots(1, 3, figsize=(18, 7.8))
    fig.suptitle(
        "Figure 2. Spatial distribution of HIV prevalence and poverty incidence across Ghana districts",
        y=0.96,
    )
    panels = [
        ("HIV_Prev_Total_pct", "A. HIV prevalence, total", "YlOrRd", "%"),
        ("HIV_Prev_Women_pct", "B. HIV prevalence, women", "YlOrRd", "%"),
        ("Poverty_Incidence_pct", "C. Poverty incidence", "YlGnBu", "%"),
    ]
    for ax, (column, title, cmap, label) in zip(axes, panels):
        plot_numeric_panel(ax, gdf, column, title, cmap, label)
    add_footer(
        fig,
        "Source: Ghana DHS 2014 for HIV prevalence; Ghana Population & Housing Census 2021 for poverty. "
        "HIV values are DHS regional estimates mapped to constituent districts.",
        y=0.055,
    )
    fig.subplots_adjust(left=0.03, right=0.98, top=0.84, bottom=0.12, wspace=0.18)
    save_figure(fig, "fig2_hiv_poverty_choropleth")


def figure_3(gdf):
    fig, axes = plt.subplots(2, 3, figsize=(18, 12.5))
    fig.suptitle(
        "Figure 3. Spatial distribution of socioeconomic and behavioural determinants across Ghana districts",
        y=0.965,
    )
    panels = [
        ("VCT_Women_pct", "A. VCT uptake, women", "Greens", "%"),
        ("Condom_Use_Women_pct", "B. Condom use, women", "Purples", "%"),
        ("Edu_Secondary_Women_pct", "C. Female secondary education", "Blues", "%"),
        ("Illiteracy_Rate_pct", "D. Illiteracy rate", "Oranges", "%"),
        ("Uninsured_Rate_pct", "E. Uninsured population", "Reds", "%"),
        ("Wife_Beating_Accept_pct", "F. Wife-beating acceptance", "RdPu", "%"),
    ]
    for ax, (column, title, cmap, label) in zip(axes.ravel(), panels):
        plot_numeric_panel(ax, gdf, column, title, cmap, label)
    add_footer(
        fig,
        "Source: Ghana DHS 2022/2014 and Ghana Population & Housing Census 2021. "
        "VCT uptake, condom use, and wife-beating acceptance are DHS regional estimates.",
        y=0.04,
    )
    fig.subplots_adjust(left=0.025, right=0.985, top=0.90, bottom=0.09, wspace=0.16, hspace=0.16)
    save_figure(fig, "fig3_determinants_choropleth")


def figure_4(gdf):
    colors = {
        "HH": "#c0392b",
        "LL": "#2980b9",
        "HL": "#e67e22",
        "LH": "#82c0e8",
        "NS": "#d9d9d9",
    }
    labels = {
        "HH": "High-High",
        "LL": "Low-Low",
        "HL": "High-Low",
        "LH": "Low-High",
        "NS": "Not significant",
    }
    order = ["HH", "LL", "HL", "LH", "NS"]
    counts = gdf["LISA_Cluster_Type"].value_counts().to_dict()

    fig, ax = plt.subplots(figsize=(9.2, 13))
    for cls in order:
        subset = gdf.loc[gdf["LISA_Cluster_Type"] == cls]
        if subset.empty:
            continue
        subset.plot(
            ax=ax,
            color=colors[cls],
            edgecolor="white",
            linewidth=0.25,
        )
    style_map_axis(ax, gdf, pad=0.025)
    add_map_furniture(ax, gdf)
    ax.set_title(
        "Figure 4. LISA cluster map of HIV prevalence, Ghana districts\n"
        "(Rook contiguity, 999 permutations, p < 0.05)",
        pad=16,
    )
    handles = [
        mpatches.Patch(color=colors[cls], label=f"{labels[cls]} (n={counts.get(cls, 0)})")
        for cls in order
    ]
    handles[-1] = mpatches.Patch(
        color=colors["NS"],
        label=f"Not significant (n={counts.get('NS', 0)} polygons; 147 districts incl. Guan)",
    )
    ax.legend(
        handles=handles,
        title="LISA cluster class",
        loc="lower left",
        bbox_to_anchor=(1.01, 0.04),
        frameon=True,
        fontsize=9,
        title_fontsize=10,
    )
    ax.text(
        0.02,
        0.98,
        "Cluster statistic: Local Moran's I\nSpatial weights: rook contiguity\nSignificance: p < 0.05",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox=dict(facecolor="white", edgecolor="0.72", alpha=0.88, boxstyle="round,pad=0.3"),
    )
    add_footer(
        fig,
        f"{SOURCE_BOUNDARY_NOTE} Analysis: PySAL/esda, seed=42. "
        "HIV prevalence is a regional DHS estimate mapped to district boundaries.",
    )
    save_figure(fig, "fig4_lisa_cluster_map")


def main():
    gdf = load_map_frame()
    figure_1(gdf)
    figure_2(gdf)
    figure_3(gdf)
    figure_4(gdf)


if __name__ == "__main__":
    main()
