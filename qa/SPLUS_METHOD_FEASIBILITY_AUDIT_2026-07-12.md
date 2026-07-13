# S+ Method Feasibility Audit - Project 2
Date: 2026-07-12

## Data Reality
The listed source files were profiled before expanding the methods.

- `hiv-prevalence_subnational_gha.csv`: DHS regional HIV biomarker estimates for 2003 and 2014 only; 11 location labels per year, not district data.
- `hiv-behavior_subnational_gha.csv`, `hiv-knowledge_subnational_gha.csv`, `hiv-counseling-and-testing_subnational_gha.csv`, `hiv-attitudes_subnational_gha.csv`: DHS regional indicators, including 2022 post-reorganisation regional labels; not district measurements.
- `Master Sheet.xlsx`: district-level Census-style socioeconomic variables for 261 district records.
- `Ghana_New_260_District.geojson`: 260 boundary polygons, requiring the existing 261-to-260 reconciliation.
- WHO/GHO files for HIV, TB, workforce, health systems, financing, and STI: Ghana/Africa national or regional time series, not Ghana district or Ghana region observations.

## Supported Methods
- Global Moran's I: supported as a spatial summary of mapped regional HIV estimates, with anti-conservative p-value caveat.
- LISA / Local Moran's I: supported as district-boundary visualisation of regional clustering, not independent district hotspot proof.
- Getis-Ord Gi*: supported with the same caveat.
- Spatial lag regression: supported as ecological modelling, with strong warning that outcome and several predictors are region-constant.
- LASSO and Random Forest: supported only as exploratory ecological prediction, preferably paired with district-only sensitivity models.
- SHAP: supported only as exploratory model explanation, not causal determinant evidence.
- Leave-one-region-out spatial CV: supported and preferable to random 10-fold CV.

## Conditional Or Not Supported
- Bivariate LISA HIV x TB: not supported from the listed TB file because it is a national/Africa time series, not Ghana district or region TB data. Use only if a Ghana district/region TB dataset is supplied.
- GWR: not recommended. The HIV outcome has only 9 unique regional values across 261 districts; GWR would mainly model artefacts of regional assignment.
- Spatial error model: possible as sensitivity only if reported as exploratory; it does not solve regional outcome granularity.
- XGBoost / LightGBM / stacked ensemble: not recommended for the main manuscript. With 9 outcome values and region-constant predictors, these methods would add complexity without new epidemiological credibility.
- SMOTE: not appropriate for continuous HIV prevalence regression. It could only be justified for a clearly defined hotspot classification task, which this manuscript should not foreground.
- 10-fold random CV: not acceptable as the primary validation strategy because district rows are not independent when the outcome is regional. Leave-one-region-out is the correct headline validation.

## S+ Editorial Decision
The S+ version should not add every advanced method named in the proposal. The stronger scientific choice is to explicitly reject methods that the data cannot support and present a smaller, cleaner, reviewer-resistant analysis.

## Required Manuscript Language
Use:

> We reviewed national WHO/GHO HIV, tuberculosis, health-workforce, health-financing, and STI files, but did not include them in district-level spatial models because they contain national/Africa time-series observations rather than Ghanaian district or region observations.

Use:

> All local-cluster and model results are interpreted as ecological regional patterns rendered on district geometry, with district-only sensitivity analyses used to test whether the broad spatial gradient persists among genuinely district-varying covariates.

Avoid:

> district-level HIV determinants, district HIV hotspots, XGBoost-confirmed predictors, SMOTE-balanced hotspot classification, or HIV x TB district co-clustering.

