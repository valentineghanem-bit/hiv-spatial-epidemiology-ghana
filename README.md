# Regional HIV Spatial Patterns Mapped Across Ghanaian District Boundaries

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem, MSc Public Health, MSc Data Science  
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)  
**Reporting standard:** STROBE; ecological cross-sectional spatial analysis  
**Target journal:** BMC Public Health
**Status:** Manuscript in preparation as a BMC Public Health Research article
**Repository:** `hiv-spatial-epidemiology-ghana`

## 1. Abstract

This repository contains the reproducible analysis for a Ghana HIV spatial epidemiology study using Ghana DHS regional HIV estimates, DHS behavioural indicators, 2021 Census socioeconomic covariates, and GSS district boundaries. The central finding is a strong south-north HIV prevalence gradient when regional DHS estimates are mapped across district boundaries. The manuscript is deliberately conservative: HIV prevalence, VCT uptake, and wife-beating acceptance are regional estimates, not direct district measurements. District maps are therefore communication geometry, not proof of district-resolved HIV differences.

## 2. Research Question & Aims

The study asks how HIV prevalence varies geographically in Ghana when public regional DHS estimates are linked to district boundaries, and how far the observed pattern is explained by behavioural, socioeconomic, and spatial structure.

The aims are to quantify HIV spatial autocorrelation, compare spatial lag and spatial error regression, test GWR feasibility under regional predictor granularity, compare LASSO and Random Forest/SHAP sensitivity models, and define what public aggregate DHS/Census data can support without overclaiming district inference.

## 3. Methods Summary

| Method | Tool | Purpose |
|---|---|---|
| Global Moran's I | PySAL/esda | National spatial autocorrelation |
| LISA and bivariate LISA | PySAL/esda | Local clustering and local covariate association |
| Getis-Ord Gi* | PySAL/esda | Hotspot and coldspot cross-check |
| Spatial lag model | spreg | Spatial dependence model |
| Spatial error model | spreg | LM-preferred residual spatial dependence model |
| GWR | mgwr | Local non-stationarity among district-varying predictors |
| LASSO | scikit-learn | Regularised feature selection |
| Random Forest + SHAP | scikit-learn, shap | Predictive sensitivity and interpretability |

## 4. Data Sources

| Source | Year | Level | Local file |
|---|---:|---|---|
| Ghana DHS HIV biomarker table | 2014 | Regional, 10-region structure | `hiv-prevalence_subnational_gha.csv` |
| Ghana DHS behavioural indicators | 2022 | Regional, 16-region structure | `hiv-behavior_*`, `hiv-knowledge_*`, `hiv-counseling-and-testing_*`, `hiv-attitudes_*` |
| Ghana Population and Housing Census | 2021 | District | `Master Sheet.xlsx` |
| Ghana Statistical Service boundaries | 2023 | 261 district records; Guan shares display geometry for map rendering | `Ghana_New_260_District.geojson` |

## 5. Key Findings

| Metric | Value |
|---|---:|
| Analytical records | 261 census districts |
| HIV prevalence granularity | 9 distinct DHS regional values |
| Global Moran's I for HIV prevalence | 0.920, permutation p = 0.001 |
| LISA High-High mapped units | 59 |
| LISA Low-Low mapped units | 51 |
| Getis-Ord Gi* hotspots/coldspots | 53 / 53 |
| Spatial lag pseudo-R2 | 0.926 |
| Spatial error lambda | 0.923 |
| Spatial error pseudo-R2 | 0.808 |
| Robust LM-error vs LM-lag | 182.4 vs 4.6 |
| District-only GWR R2 | 0.956; CV bandwidth check R2 = 0.957 |
| Random Forest leave-one-region-out R2 | 0.611 |

## 6. Repository Structure

```text
hiv-spatial-epidemiology-ghana/
  README.md
  CITATION.cff
  DATA_CORRECTION_NOTE.md
  LICENSE
  requirements.txt
  analysis/
    spatial_analysis_pipeline.py
    gwr_spatial_error_analysis.py
  dashboard/
    HIV_Spatial_Ghana_Dashboard.html
    app.py
  poster/
    HIV_Spatial_Ghana_Poster.html
  docs/
    district_crosswalk_261_to_260.csv
  outputs/
    data/
    figures/
    figures_cambridge/
  qa/
  tests/
```

## 7. Reproducibility

### 7.1 Requirements

Install the Python packages in `requirements.txt`. The analysis was developed with Python 3.13 locally; Python 3.12+ is expected to work if geospatial wheels are available.

### 7.2 Clone & Install

```bash
git clone https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana.git
cd hiv-spatial-epidemiology-ghana
pip install -r requirements.txt
```

### 7.3 Run The Analytical Pipeline

```bash
python analysis/spatial_analysis_pipeline.py
python analysis/gwr_spatial_error_analysis.py
```

### 7.4 Run The Test Suite

```bash
python -m pytest -q
```

Current local QA result: `29 passed`.

### 7.5 Launch The Interactive Dash Application

```bash
cd dashboard
python app.py
```

### 7.6 Open The Static HTML Dashboard

Open `dashboard/HIV_Spatial_Ghana_Dashboard.html` directly in a browser. No external JavaScript library is required.

## 8. Outputs

| Output | Description |
|---|---|
| `outputs/data/Ghana_HIV_Spatial_Analysis_MASTER.csv` | Final analytical dataset |
| `outputs/data/spatial_error_model_results.csv` | Spatial error model coefficients |
| `outputs/data/gwr_coefficient_summary.csv` | GWR local coefficient summary |
| `outputs/data/gwr_local_r2.csv` | District-level local R2 values from district-only GWR |
| `outputs/data/gwr_spatial_error_metadata.txt` | GWR feasibility and spatial error summary |
| `outputs/figures/` | PNG manuscript figures prepared at publication-readable scale for BMC review |
| `outputs/figures_cambridge/` | TIFF exports retained from an earlier journal-formatting pass; BMC accepts TIFF, PNG, PDF, EPS and other standard figure formats at legible final size |
| `qa/` | Editorial, guideline, and submission-readiness audits |

## 8a. Downloadable Artefacts (HTML)

| Artefact | View on GitHub | Live preview | Direct download |
|---|---|---|---|
| Interactive dashboard | [View](https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/blob/main/dashboard/HIV_Spatial_Ghana_Dashboard.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/blob/main/dashboard/HIV_Spatial_Ghana_Dashboard.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/main/dashboard/HIV_Spatial_Ghana_Dashboard.html) |
| Conference poster | [View](https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/blob/main/poster/HIV_Spatial_Ghana_Poster.html) | [Preview](https://htmlpreview.github.io/?https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/blob/main/poster/HIV_Spatial_Ghana_Poster.html) | [Download](https://raw.githubusercontent.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana/main/poster/HIV_Spatial_Ghana_Poster.html) |

## 9. Reporting Standard

The manuscript follows STROBE principles for observational research and is structured for a BMC Public Health Research article: structured abstract, Background, Methods, Results, Discussion, Conclusions, List of abbreviations, and Declarations. The core limitation is stated plainly throughout: regional DHS HIV and behavioural estimates are displayed across district boundaries but are not independent district measurements.

## 10. Ethical Statement

The study uses publicly available, de-identified, aggregate secondary data. No individual-level records were accessed. No primary data were collected. No ethics approval was required for the repository analysis.

## 11. Citation

Ghanem VG. Regional HIV spatial patterns mapped across Ghanaian district boundaries: an ecological spatial analysis. 2026.

```bibtex
@misc{ghanem2026hivspatialghana,
  author = {Ghanem, Valentine Golden},
  title = {Regional HIV spatial patterns mapped across Ghanaian district boundaries},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/valentineghanem-bit/hiv-spatial-epidemiology-ghana},
  note = {STROBE-aligned ecological spatial analysis}
}
```

## 12. License

Code is released under the MIT License. Figures and public-facing outputs should be cited to the repository and underlying public data sources.

## 13. Author & Contact

Valentine Golden Ghanem  
Ghana COCOBOD Cocoa Clinic, Accra, Ghana  
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

## 14. Acknowledgements

This repository depends on public data infrastructure from the Ghana Statistical Service, the Ghana Demographic and Health Survey programme, and open-source geospatial and statistical software communities.
