# Data Correction Note — 2026-07-12

**Status:** Pre-publication correction. No external release of this repository preceded this fix.

## What was wrong

The spatial statistics pipeline (`outputs/data/LISA_Results.csv` and everything
derived from it — Global Moran's I, LISA, Bivariate LISA, Getis-Ord Gi*, and
the spatial lag regression) was built from a district-name join that did not
reconcile the census attribute data's district names against the GSS 2023
boundary file's polygon labels. This produced two compounding defects:

1. **10 districts were duplicated**, each appearing twice in `LISA_Results.csv`
   with materially different, sometimes contradictory Local Moran's I values,
   p-values, and significance flags for the same district (e.g. Tano South
   Municipal was flagged non-significant, p=0.482, in one row and significant,
   p=0.03, in the other).
2. **11 real districts were silently dropped** from the spatial analysis
   entirely (Bolgatanga East, Guan, Dormaa Central Municipal, Kwahu West
   Municipal, Cape Coast Metropolitan, Akwapim North/South Municipal, West
   Akim Municipal, Awutu Senya East Municipal, Kasena Nankana Municipal,
   Sissala East Municipal), because their census-derived names did not
   string-match the boundary file's polygon labels.

The Master CSV, README, CITATION.cff, sync-manifest, dashboard, and poster
all separately claimed "260 districts" as if this were a deliberate,
documented scope — it was not. The true resolved count in the pre-fix
`LISA_Results.csv` was 250 unique districts, 10 of them internally
contradictory.

LASSO, Random Forest, and SHAP were **not** affected — those aspatial models
run directly on the 261-row census attribute table and do not require
geometry, so their published R²/RMSE/MAE/feature-importance figures were
already correct and are essentially unchanged after the fix.

## What was fixed

`analysis/spatial_analysis_pipeline.py` (new; replaces the removed
`analysis/build_master_dataset.py`) joins the 261-district census attribute
table to the 260-polygon GSS boundary file via `docs/district_crosswalk_261_to_260.csv`
— a vetted crosswalk already in production use across Projects 15, 16, 18–23.
Two additional district-name corrections specific to this project's copy of
the boundary file were identified and applied (Awutu Senya West → `AWUTU
SENYA`, Sagnarigu Municipal → `SAGNERIGU`; both have standalone polygons in
this GeoJSON). The one genuine structural gap — **Guan** (created 2018 from
Krachi East Municipal; no distinct 2023 boundary polygon exists) — shares its
parent polygon's geometry; the two districts' values are combined by
`Total_Pop`-weighted mean for geometry-dependent statistics only. All 261
districts are retained with their own independent covariate values in the
Master CSV; a `Spatial_Unit_Note` column documents the shared-geometry case
for the two affected rows.

All spatial statistics were recomputed with a fixed seed (42) for
reproducibility. Full before/after comparison:

| Statistic | Published (broken) | Corrected |
|---|---|---|
| N districts | 260 (claimed; actually 250 resolved) | 261 |
| Global Moran's I (KNN k=4) | 0.907, p<0.001 | 0.920, p=0.001 |
| LISA significant districts | 110 (59 LH + 51 HL, per README) / 113 (per raw JSON, internally inconsistent) | 114 (59 HH + 51 LL + 4 HL + 0 LH) |
| LISA cluster narrative | "boundary-transition" (LH/HL dominant) | classic hotspot/coldspot (HH/LL dominant) — verified: HH mean 2.73% HIV vs 1.91% national mean; LL mean 0.41% |
| Getis-Ord Gi* | 0 hotspots, 0 coldspots (all non-significant — clearly broken) | 53 hotspots, 53 coldspots, 154 not significant |
| Spatial lag rho / pseudo-R² | 0.596 / 0.927 | 0.606 / 0.926 (materially unchanged) |
| Spatial lag: PMTCT knowledge | non-significant, p=0.489 | significant, p=0.048 |
| Bivariate LISA significant locations | "4" (one per pair — a degenerate global-stat miscount) | 104 / 116 / 89 / 111 per pair (proper local bivariate LISA) |
| LASSO R² | 0.9328 | 0.9328 (unchanged — was never broken) |
| Random Forest R² | 0.6108 | 0.6108 (unchanged — was never broken) |
| SHAP top 3 | VCT uptake, wife-beating acceptance, secondary education | unchanged |

The qualitative finding changes from "boundary-transition zones dominate" to
"classic hotspot (southern belt) / coldspot (northern belt) clustering" —
this is the epidemiologically expected pattern for Ghana's HIV prevalence
gradient and is corroborated by the Getis-Ord Gi* results, which independently
found 53/53 symmetric hot/coldspots after the fix (versus zero of either
before).

Figures `fig4_lisa_cluster_map.png` and `fig5_morans_scatterplot.png` were
regenerated from the corrected data; all other figures were unaffected and
left untouched. `outputs/data/Ghana_HIV_Analysis_Dataset_260districts.csv`
keeps its original filename (it is an intermediate input, not a citable
deliverable) — it in fact already contained all 261 census districts.

## Files affected

`outputs/data/Ghana_HIV_Spatial_Analysis_MASTER.csv`, `LISA_Results.csv`,
`Morans_I_Results.csv`, `Getis_Ord_Results.csv`, `Bivariate_LISA_Results.csv`
(+ new `Bivariate_LISA_Local_Results.csv`), `Spatial_Lag_Regression_Results.csv`,
`lasso_results.csv`, `rf_cv_results.csv`, `shap_values.csv`, `shap_summary.csv`,
`model_comparison.csv`, `spatial_analysis_results.json`, `ml_analysis_results.json`,
`Master/Ghana_HIV_Spatial_Analysis_MASTER.csv`, `outputs/figures/fig4_*.png`,
`outputs/figures/fig5_*.png`, README.md, CITATION.cff, sync-manifest.json,
dashboard/poster HTML.
