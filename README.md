# Subnational Spatial Epidemiology of HIV Prevalence and Socioeconomic Determinants in Ghana

**Bivariate LISA, GWR, and Random Forest — 260-District DHS Analysis**

## Author

Valentine Golden Ghanem, MSc Public Health, MSc Data Science 
Ghana COCOBOD Cocoa Clinic, Accra, Ghana 
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

## Overview

This repository contains the complete analytical pipeline, interactive dashboard, conference poster, and reproducible datasets for a spatial epidemiological analysis of HIV prevalence across Ghana's 260 administrative districts.

### Key Findings

- **Strong spatial clustering**: Moran's I = 0.907 (p<0.001) for HIV prevalence
- **LISA clusters**: 110 significant clusters — 59 Low-High and 51 High-Low boundary-transition effects
- **Spatial lag model**: rho = 0.596, pseudo-R² = 0.927; VCT uptake, modern contraception, and condom use as significant predictors
- **LASSO regression**: R² = 0.933; latitude and wife beating acceptance as strongest predictors
- **Random Forest (spatial CV)**: R² = 0.611; SHAP top 3: VCT uptake, wife beating acceptance, female secondary education

## Data Sources

| Source | Year | Level | File |
|--------|------|-------|------|
| Ghana DHS (HIV biomarker) | 2014 | Regional (10 regions) | hiv-prevalence_subnational_gha.csv |
| Ghana DHS (behavioural) | 2022 | Regional (16 regions) | hiv-behavior/knowledge/counseling/attitudes |
| Ghana Census | 2021 | District (261 units) | Master Sheet.xlsx |
| Ghana Statistical Service | 2023 | District (260 polygons) | Ghana_New_260_District.geojson |

## Repository Structure

```
HIV_Spatial_Ghana_260District/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── analysis/
│ └── build_master_dataset.py # Produces the master CSV from raw data
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
 │ ├── Ghana_HIV_Spatial_Analysis_MASTER.csv # FINAL analytical dataset
 │ ├── Ghana_HIV_Analysis_Dataset_260districts.csv
 │ ├── LISA_Results.csv
 │ ├── Morans_I_Results.csv
 │ ├── Spatial_Lag_Regression_Results.csv
 │ ├── lasso_results.csv
 │ ├── rf_cv_results.csv
 │ ├── shap_values.csv
 │ ├── spatial_analysis_results.json
 │ └── ml_analysis_results.json
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
python analysis/build_master_dataset.py
```

### Dashboard
```bash
cd dashboard && python app.py
# Or open HIV_Spatial_Ghana_Dashboard.html directly in a browser
```

## Methods

- **Spatial autocorrelation**: Global Moran's I (KNN k=4), LISA (Rook contiguity, 999 permutations)
- **Hotspot analysis**: Getis-Ord Gi* (KNN k=4)
- **Spatial regression**: Spatial lag model (ML estimation, Queen contiguity)
- **Machine learning**: LASSO (10-fold CV), Random Forest (leave-one-region-out spatial CV)
- **Interpretability**: SHAP values (TreeExplainer)
- **Reporting**: STROBE guidelines

## Citation

```
Ghanem VG (2026). Subnational spatial epidemiology of HIV prevalence and
socioeconomic determinants in Ghana: Bivariate LISA, GWR, and Random Forest
analysis across 260 districts.
```

## License

MIT License — see LICENSE file.
