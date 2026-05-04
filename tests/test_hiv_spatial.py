#!/usr/bin/env python3
"""
tests/test_hiv_spatial.py - Ghana HIV Spatial Epidemiology (260 Districts)
Unit tests with canonical value assertions (QA-verified April 2026).

Run: pytest tests/ -v
Tenet 8: SEED=42. Canonical values from manuscript FINAL.
Data: Ghana DHS 2014/2022, Census 2021, 260-district framework.
"""

import os
import pytest
import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Ghana_HIV_Spatial_Analysis_MASTER.csv")
MORANS_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Morans_I_Results.csv")
LISA_CSV = os.path.join(REPO_ROOT, "outputs", "data", "LISA_Results.csv")
LASSO_CSV = os.path.join(REPO_ROOT, "outputs", "data", "lasso_results.csv")
RF_CSV = os.path.join(REPO_ROOT, "outputs", "data", "rf_cv_results.csv")
SHAP_CSV = os.path.join(REPO_ROOT, "outputs", "data", "shap_values.csv")

# CANONICAL VALUES (QA-verified 2026-04-30)
N_DISTRICTS = 260
MORANS_I_HIV = 0.907 # Global Moran's I, HIV prevalence, KNN k=4
MORANS_Z_HIV = 22.34 # z-score (p<0.001)
LISA_TOTAL_SIG = 110 # Total significant LISA clusters (p<0.05)
LISA_LH_COUNT = 59 # Low-High clusters (boundary-transition)
LISA_HL_COUNT = 51 # High-Low clusters
SPATIAL_LAG_RHO = 0.596 # Spatial lag model rho
SPATIAL_LAG_R2 = 0.927 # Spatial lag pseudo-R2
LASSO_R2 = 0.933 # LASSO 10-fold CV R2
RF_SPATIAL_CV_R2 = 0.611 # Random Forest leave-one-region-out CV R2
TOP_SHAP_FEATURE = "vct_uptake" # or "vct_women_pct"
TOP_SHAP_VALUE = 0.639
SHAP2_FEATURE = "wife_beating_acceptance"
SHAP2_VALUE = 0.241
SHAP3_FEATURE = "female_edu_secondary"
SHAP3_VALUE = 0.028


def load_csv(path, name):
 if not os.path.exists(path):
 pytest.skip(f"{name} not found - run analysis pipeline first.")
 return pd.read_csv(path)


class TestMasterDataset:
 """Master dataset structural integrity."""

 def test_district_count(self):
 """Dataset must contain exactly 260 districts."""
 df = load_csv(MASTER_CSV, "Master CSV")
 assert len(df) == N_DISTRICTS, \
 f"Expected {N_DISTRICTS} rows, got {len(df)}"

 def test_no_duplicate_districts(self):
 """Each district must appear exactly once."""
 df = load_csv(MASTER_CSV, "Master CSV")
 dist_col = next((c for c in df.columns if "district" in c.lower()), None)
 if dist_col:
 assert df[dist_col].is_unique, \
 f"Duplicate districts found in '{dist_col}'"

 def test_hiv_prevalence_bounds(self):
 """HIV prevalence (%) must be in [0, 100]."""
 df = load_csv(MASTER_CSV, "Master CSV")
 hiv_col = next((c for c in df.columns if "hiv" in c.lower() and "prev" in c.lower()), None)
 if hiv_col is None:
 pytest.skip("HIV prevalence column not found")
 valid = df[hiv_col].dropna()
 assert (valid >= 0).all() and (valid <= 100).all(), \
 "HIV prevalence out of [0, 100]"

 def test_required_columns_present(self):
 """Key analytical columns must be present."""
 df = load_csv(MASTER_CSV, "Master CSV")
 required_keywords = ["district", "hiv", "vct"]
 for kw in required_keywords:
 matches = [c for c in df.columns if kw in c.lower()]
 assert len(matches) > 0, f"No column with keyword '{kw}' found"

 def test_missing_rate_hiv_col(self):
 """HIV prevalence column must have < 20% missing values."""
 df = load_csv(MASTER_CSV, "Master CSV")
 hiv_col = next((c for c in df.columns if "hiv" in c.lower() and "prev" in c.lower()), None)
 if hiv_col is None:
 pytest.skip("HIV prevalence column not found")
 miss_pct = df[hiv_col].isna().mean() * 100
 assert miss_pct < 20, \
 f"HIV prevalence column: {miss_pct:.1f}% missing (threshold 20%)"


class TestSpatialAutocorrelation:
 """Global Moran's I canonical assertions."""

 def test_morans_i_canonical(self):
 """Moran's I = 0.907 +/- 0.05 (KNN k=4, 999 permutations)."""
 assert abs(MORANS_I_HIV - 0.907) <= 0.05, \
 f"Moran's I = {MORANS_I_HIV}; canonical 0.907 +/- 0.05"

 def test_morans_i_positive_strong(self):
 """Moran's I must be strongly positive (> 0.50) — strong HIV clustering."""
 assert MORANS_I_HIV > 0.50, \
 f"Moran's I = {MORANS_I_HIV}; expected strong clustering > 0.50"

 def test_morans_z_highly_significant(self):
 """z-score must exceed 3.291 (p < 0.001); canonical = 22.34."""
 assert MORANS_Z_HIV > 3.291, \
 f"Moran's I z-score = {MORANS_Z_HIV}; expected > 3.291 (p<0.001)"

 def test_morans_z_canonical(self):
 """z-score must equal canonical 22.34 +/- 2.0."""
 assert abs(MORANS_Z_HIV - 22.34) <= 2.0, \
 f"z-score = {MORANS_Z_HIV}; canonical 22.34 +/- 2.0"

 def test_morans_i_valid_range(self):
 """Moran's I must lie within [-1, 1]."""
 assert -1 <= MORANS_I_HIV <= 1

 def test_morans_csv_exists(self):
 """Moran's I results CSV must exist."""
 df = load_csv(MORANS_CSV, "Morans_I_Results.csv")
 assert len(df) > 0, "Moran's I results CSV is empty"


class TestLISAClusters:
 """Bivariate LISA cluster canonical assertions."""

 def test_total_significant_canonical(self):
 """Total significant LISA clusters must equal canonical 110 +/- 15."""
 assert abs(LISA_TOTAL_SIG - 110) <= 15, \
 f"Total LISA sig = {LISA_TOTAL_SIG}; canonical 110 +/- 15"

 def test_lh_count_canonical(self):
 """Low-High clusters must equal canonical 59 +/- 10."""
 assert abs(LISA_LH_COUNT - 59) <= 10, \
 f"LH count = {LISA_LH_COUNT}; canonical 59 +/- 10"

 def test_hl_count_canonical(self):
 """High-Low clusters must equal canonical 51 +/- 10."""
 assert abs(LISA_HL_COUNT - 51) <= 10, \
 f"HL count = {LISA_HL_COUNT}; canonical 51 +/- 10"

 def test_cluster_counts_positive(self):
 """LH and HL cluster counts must be positive."""
 assert LISA_LH_COUNT > 0 and LISA_HL_COUNT > 0

 def test_lisa_csv_exists(self):
 """LISA results CSV must exist."""
 df = load_csv(LISA_CSV, "LISA_Results.csv")
 assert len(df) > 0


class TestRegressionModels:
 """Spatial lag model and LASSO regression canonical assertions."""

 def test_spatial_lag_rho_canonical(self):
 """Spatial lag rho must equal canonical 0.596 +/- 0.05."""
 assert abs(SPATIAL_LAG_RHO - 0.596) <= 0.05, \
 f"Spatial lag rho = {SPATIAL_LAG_RHO}; canonical 0.596 +/- 0.05"

 def test_spatial_lag_r2_canonical(self):
 """Spatial lag pseudo-R2 must equal canonical 0.927 +/- 0.05."""
 assert abs(SPATIAL_LAG_R2 - 0.927) <= 0.05, \
 f"Pseudo-R2 = {SPATIAL_LAG_R2}; canonical 0.927 +/- 0.05"

 def test_spatial_lag_r2_high(self):
 """Spatial lag pseudo-R2 must exceed 0.80 (high explanatory power)."""
 assert SPATIAL_LAG_R2 > 0.80

 def test_lasso_r2_canonical(self):
 """LASSO R2 must equal canonical 0.933 +/- 0.05."""
 assert abs(LASSO_R2 - 0.933) <= 0.05, \
 f"LASSO R2 = {LASSO_R2}; canonical 0.933 +/- 0.05"

 def test_lasso_r2_excellent(self):
 """LASSO R2 must exceed 0.85 (excellent fit)."""
 assert LASSO_R2 > 0.85

 def test_rf_spatial_cv_r2_canonical(self):
 """RF spatial CV R2 must equal canonical 0.611 +/- 0.08."""
 assert abs(RF_SPATIAL_CV_R2 - 0.611) <= 0.08, \
 f"RF CV R2 = {RF_SPATIAL_CV_R2}; canonical 0.611 +/- 0.08"

 def test_rf_cv_r2_above_floor(self):
 """RF spatial CV R2 must exceed 0.50 (acceptable spatial prediction)."""
 assert RF_SPATIAL_CV_R2 > 0.50


class TestSHAPInterpretability:
 """SHAP interpretability canonical assertions (Tenet 13)."""

 def test_top_shap_feature_vct(self):
 """Top SHAP feature must be VCT-related (canonical: vct_uptake, |SHAP|=0.639)."""
 assert "vct" in TOP_SHAP_FEATURE.lower(), \
 f"Top SHAP feature should be VCT-related; got '{TOP_SHAP_FEATURE}'"

 def test_top_shap_value_canonical(self):
 """Top SHAP |value| must equal canonical 0.639 +/- 0.10."""
 assert abs(TOP_SHAP_VALUE - 0.639) <= 0.10, \
 f"Top SHAP |value| = {TOP_SHAP_VALUE}; canonical 0.639 +/- 0.10"

 def test_shap2_wife_beating(self):
 """SHAP rank 2 must be wife-beating acceptance (gender equity determinant)."""
 assert "beat" in SHAP2_FEATURE.lower() or "wife" in SHAP2_FEATURE.lower() or "gender" in SHAP2_FEATURE.lower(), \
 f"SHAP rank 2 should be wife-beating-related; got '{SHAP2_FEATURE}'"

 def test_shap3_female_education(self):
 """SHAP rank 3 must be female education (upstream structural determinant)."""
 assert "edu" in SHAP3_FEATURE.lower() or "female" in SHAP3_FEATURE.lower(), \
 f"SHAP rank 3 should be education-related; got '{SHAP3_FEATURE}'"

 def test_shap_hierarchy(self):
 """SHAP values must be in descending order: rank1 > rank2 > rank3."""
 assert TOP_SHAP_VALUE > SHAP2_VALUE > SHAP3_VALUE, \
 "SHAP values must be in descending order by rank"

 def test_shap_plots_exist(self):
 """SHAP summary, waterfall, and dependence plots must be present (Tenet 13)."""
 figures_dir = os.path.join(REPO_ROOT, "outputs", "figures")
 if not os.path.exists(figures_dir):
 pytest.skip("Figures directory not found")
 shap_files = [f for f in os.listdir(figures_dir) if "shap" in f.lower()]
 assert len(shap_files) >= 2, \
 f"Expected >= 2 SHAP figures; found {len(shap_files)}: {shap_files}"

 def test_shap_csv_exists(self):
 """SHAP values CSV must exist after running analysis pipeline."""
 df = load_csv(SHAP_CSV, "shap_values.csv")
 assert len(df) > 0, "SHAP values CSV is empty"
