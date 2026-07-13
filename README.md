# Regional HIV Spatial Patterns Mapped Across Ghanaian District Boundaries

**Bivariate LISA, Spatial Lag/Error Regression, Geographically Weighted Regression, and Random Forest — 261-District DHS Analysis**

*Formerly titled "Subnational Spatial Epidemiology of HIV Prevalence and Socioeconomic Determinants in Ghana"; retitled 2026-07-13 so the repository name matches the analysis's actual resolution — see the methodological limitation below.*

## Author

Valentine Golden Ghanem, MSc Public Health, MSc Data Science 
Ghana COCOBOD Cocoa Clinic, Accra, Ghana 
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

## Overview

This repository contains the complete analytical pipeline, interactive dashboard, conference poster, and reproducible datasets for a spatial epidemiological analysis of HIV prevalence across all 261 of Ghana's census districts (261 districts share 260 unique GSS 2023 boundary polygons — see [DATA_CORRECTION_NOTE.md](DATA_CORRECTION_NOTE.md) for the district-geometry reconciliation and a full before/after audit of a pre-publication data-join defect that was caught and corrected on 2026-07-12).

### ⚠ Important methodological limitation: outcome and top predictors are region-level, not district-level

HIV prevalence (the outcome variable) is the 2014 Ghana DHS **regional** (10-region) biomarker estimate, and the two strongest predictors below — VCT uptake and wife-beating acceptance — are 2022 DHS **regional** (16-region) estimates. Ghana's DHS survey design does not produce district-level HIV biomarker or behavioural data; every district within a region is assigned its region's value for these three variables. Only the Census-derived socioeconomic covariates (poverty, literacy, insurance, etc.) carry genuine district-level variation. This means:

- The district "choropleth" for HIV prevalence, VCT uptake, and wife-beating acceptance is a regional pattern rendered at district resolution, not an independently-measured district-level survey.
- Spatial autocorrelation statistics (Global Moran's I, LISA, Getis-Ord Gi\*) computed on these three variables are substantially inflated by this region-to-district disaggregation, since neighboring districts in the same region share identical values by construction — their permutation-based p-values should be read as anti-conservative (true effective N is closer to 10–16 than 261).
- LASSO/Random Forest R² driven by these region-level predictors likely reflects regional grouping rather than genuine district-level covariate–outcome relationships.
- **Policy targeting implications**: interventions (e.g. VCT scale-up) should be prioritized at the *region* level using these findings, not directed at individually-named districts — no district in this dataset has been shown to differ from its regional neighbors on HIV prevalence, VCT uptake, or wife-beating acceptance.

This is a data-availability constraint inherent to the DHS source, not an error in the analysis pipeline; disaggregating regional survey estimates to district level for GIS/policy mapping is a recognized practice in LMIC subnational health mapping, provided (as here) it is disclosed.

### Key Findings

- **Strong spatial clustering**: Global Moran's I = 0.920 (KNN k=4, p=0.001) for HIV prevalence — read against the regional-granularity caveat above
- **LISA clusters**: 114 significant districts — classic hotspot/coldspot pattern (59 High-High, 51 Low-Low, 4 High-Low outliers), not a boundary-transition pattern. High-High districts average 2.73% HIV prevalence vs. a 1.91% national mean; Low-Low districts average 0.41%
- **Getis-Ord Gi\***: 53 hotspots and 53 coldspots (KNN k=4); directionally consistent with the LISA hot/coldspot pattern, though not independent statistical corroboration since both are computed on the same region-block-structured outcome variable
- **Spatial lag model**: rho = 0.606, pseudo-R² = 0.926; VCT uptake, modern contraception, condom use, and PMTCT knowledge all significant predictors (Queen contiguity, ML estimation)
- **Spatial error model**: lambda = 0.923, pseudo-R² = 0.808 (same predictors as spatial lag). Lagrange multiplier diagnostics favour this specification over the spatial lag model (robust LM-error = 182.4, p < 0.001 vs. robust LM-lag = 4.6, p = 0.032), consistent with — not proof of — spatial dependence residing substantially in region-block-correlated residual structure
- **Geographically weighted regression (GWR)**: did not converge on the region-level predictor set (singular local design matrices — a numerical artefact directly illustrating the granularity limitation below, not a formal test of it). Restricted to the 7 genuinely district-level predictors, GWR converged (adaptive bandwidth 58 nearest neighbours, AICc-selected; cross-checked against an independent leave-one-out CV bandwidth search at 57 neighbours, R² = 0.957) and outperformed global OLS on the same predictors (R² = 0.956 vs. 0.840); local coefficients for latitude/longitude reversed sign across the country, with some negative local R² values flagging local-fit instability in sparse neighbourhoods
- **LASSO regression**: R² = 0.933; latitude and wife-beating acceptance as strongest predictors (13 of 19 features selected, 10-fold CV). District-only sensitivity model: R² = 0.840, leading predictor shifts to latitude
- **Random Forest (leave-one-region-out spatial CV)**: R² = 0.611; SHAP top 3: VCT uptake, wife-beating acceptance, female secondary education. District-only sensitivity model: R² = 0.677

## Data Sources

| Source | Year | Level | File |
|--------|------|-------|------|
| Ghana DHS (HIV biomarker) | 2014 | Regional (10 regions) | hiv-prevalence_subnational_gha.csv |
| Ghana DHS (behavioural) | 2022 | Regional (16 regions) | hiv-behavior/knowledge/counseling/attitudes |
| Ghana Census | 2021 | District (261 units) | Master Sheet.xlsx |
| Ghana Statistical Service | 2023 | District (260 unique boundary polygons; 1 district shares its parent's polygon — see Data Correction Note) | Ghana_New_260_District.geojson |

## Repository Structure

```
HIV_Spatial_Ghana_261District/
├── README.md
├── DATA_CORRECTION_NOTE.md # Pre-publication join-defect audit and fix (2026-07-12)
├── requirements.txt
├── .gitignore
├── LICENSE
├── docs/
│ └── district_crosswalk_261_to_260.csv # Vetted 261 census district <-> 260 polygon crosswalk
├── data/
│ └── raw/
│ └── Ghana_New_260_District.geojson # Canonical GSS 2023 boundary file
├── analysis/
│ ├── spatial_analysis_pipeline.py # Produces the master CSV + all spatial/ML outputs from raw data
│ └── gwr_spatial_error_analysis.py # GWR + spatial error model + LM specification diagnostics
├── qa/ # Editorial/council audit trail (Q1/Cambridge alignment, final verdict)
├── dashboard/
│ ├── app.py # Python Dash interactive app
│ ├── HIV_Spatial_Ghana_Dashboard.html # Self-contained HTML dashboard
│ ├── run_dashboard.command # macOS launcher
│ ├── run_dashboard.bat # Windows launcher
│ └── run_dashboard.sh # Linux launcher
├── poster/
│ └── HIV_Spatial_Ghana_Poster.html # A0 conference poster
└── outputs/
 ├── data/
 │ ├── Ghana_HIV_Spatial_Analysis_MASTER.csv # FINAL analytical dataset (261 districts)
 │ ├── Ghana_HIV_Analysis_Dataset_260districts.csv # Raw census attribute input (261 rows; retains legacy filename)
 │ ├── LISA_Results.csv
 │ ├── Bivariate_LISA_Results.csv
 │ ├── Bivariate_LISA_Local_Results.csv
 │ ├── Getis_Ord_Results.csv
 │ ├── Morans_I_Results.csv
 │ ├── Spatial_Lag_Regression_Results.csv
 │ ├── lasso_results.csv
 │ ├── rf_cv_results.csv
 │ ├── model_comparison.csv
 │ ├── shap_values.csv
 │ ├── shap_summary.csv
 │ ├── spatial_analysis_results.json
 │ ├── ml_analysis_results.json
 │ ├── spatial_error_model_results.csv
 │ ├── gwr_coefficient_summary.csv
 │ ├── gwr_local_r2.csv
 │ └── gwr_spatial_error_metadata.txt
 └── figures/
 ├── fig1_study_area_map.png
 ├── fig2_hiv_poverty_choropleth.png
 ├── fig3_determinants_choropleth.png
 ├── fig4_lisa_cluster_map.png
 ├── fig5_morans_scatterplot.png
 ├── fig6_correlation_heatmap.png
 ├── fig_shap_summary.png
 ├── fig_shap_dependence.png
 └── fig_shap_waterfall.png
```

## Reproduction

### Python analysis
```bash
pip install -r requirements.txt
python analysis/spatial_analysis_pipeline.py
python analysis/gwr_spatial_error_analysis.py
```

### Dashboard
```bash
cd dashboard && python app.py
# Or open HIV_Spatial_Ghana_Dashboard.html directly in a browser
```

## Methods

- **District-geometry reconciliation**: 261 census districts joined to 260 unique GSS 2023 boundary polygons via a vetted crosswalk (`docs/district_crosswalk_261_to_260.csv`); the one structural gap (Guan, split from Krachi East Municipal in 2018) shares its parent polygon and is combined by population-weighted mean for geometry-dependent statistics only — see [DATA_CORRECTION_NOTE.md](DATA_CORRECTION_NOTE.md)
- **Spatial autocorrelation**: Global Moran's I (KNN k=4), LISA (Rook contiguity, 999 permutations)
- **Hotspot analysis**: Getis-Ord Gi* (KNN k=4)
- **Spatial regression**: Spatial lag and spatial error models (ML estimation, Queen contiguity); specification choice justified by Lagrange multiplier diagnostics (standard and robust, both forms) computed from an OLS baseline
- **Local non-stationarity**: Geographically weighted regression (adaptive bisquare kernel; bandwidth selected by AICc and cross-checked against leave-one-out CV)
- **Machine learning**: LASSO (10-fold CV), Random Forest (leave-one-region-out spatial CV); both re-fitted on a district-only predictor subset as a sensitivity analysis
- **Interpretability**: SHAP values (TreeExplainer)
- **Reporting**: STROBE guidelines
- **Reproducibility**: fixed random seed (42) throughout

## Citation

```
Ghanem VG (2026). Regional HIV spatial patterns mapped across Ghanaian
district boundaries: Bivariate LISA, spatial lag/error regression,
geographically weighted regression, and Random Forest analysis across
261 districts.
```

## License

MIT License — see LICENSE file.
