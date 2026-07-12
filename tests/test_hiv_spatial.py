#!/usr/bin/env python3
"""
tests/test_hiv_spatial.py - Ghana HIV Spatial Epidemiology (261 Districts)

Run: pytest tests/ -v

Corrected 2026-07-12 after a pre-publication data-integrity fix (see
DATA_CORRECTION_NOTE.md): tests now load and assert against the actual
output CSVs rather than comparing hardcoded constants to themselves, which
was the previous file's defect -- the old canonical-value tests could never
fail regardless of what the pipeline actually produced.
"""

import os
import pandas as pd
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Ghana_HIV_Spatial_Analysis_MASTER.csv")
MORANS_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Morans_I_Results.csv")
LISA_CSV = os.path.join(REPO_ROOT, "outputs", "data", "LISA_Results.csv")
GETIS_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Getis_Ord_Results.csv")
LAG_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Spatial_Lag_Regression_Results.csv")
LASSO_CSV = os.path.join(REPO_ROOT, "outputs", "data", "lasso_results.csv")
RF_CSV = os.path.join(REPO_ROOT, "outputs", "data", "rf_cv_results.csv")
MODEL_COMP_CSV = os.path.join(REPO_ROOT, "outputs", "data", "model_comparison.csv")
SHAP_SUMMARY_CSV = os.path.join(REPO_ROOT, "outputs", "data", "shap_summary.csv")
SHAP_CSV = os.path.join(REPO_ROOT, "outputs", "data", "shap_values.csv")

N_DISTRICTS = 261


def load_csv(path, name):
    if not os.path.exists(path):
        pytest.skip(f"{name} not found - run analysis/spatial_analysis_pipeline.py first.")
    return pd.read_csv(path)


class TestMasterDataset:
    """Master dataset structural integrity."""

    def test_district_count(self):
        """Dataset must contain exactly 261 districts (the full census frame)."""
        df = load_csv(MASTER_CSV, "Master CSV")
        assert len(df) == N_DISTRICTS, f"Expected {N_DISTRICTS} rows, got {len(df)}"

    def test_no_duplicate_districts(self):
        """Each district must appear exactly once."""
        df = load_csv(MASTER_CSV, "Master CSV")
        assert df["District"].is_unique, "Duplicate districts found in 'District'"

    def test_hiv_prevalence_bounds(self):
        """HIV prevalence (%) must be in [0, 100]."""
        df = load_csv(MASTER_CSV, "Master CSV")
        valid = df["HIV_Prev_Total_pct"].dropna()
        assert (valid >= 0).all() and (valid <= 100).all(), "HIV prevalence out of [0, 100]"

    def test_required_columns_present(self):
        """Key analytical columns must be present."""
        df = load_csv(MASTER_CSV, "Master CSV")
        required = ["District", "Region", "HIV_Prev_Total_pct", "VCT_Women_pct",
                    "LISA_Cluster_Type", "LISA_Local_Morans_I", "Spatial_Unit_Note"]
        missing = [c for c in required if c not in df.columns]
        assert not missing, f"Missing required columns: {missing}"

    def test_no_missing_hiv_prevalence(self):
        """HIV prevalence must be populated for every district."""
        df = load_csv(MASTER_CSV, "Master CSV")
        assert df["HIV_Prev_Total_pct"].isna().sum() == 0

    def test_shared_polygon_districts_documented(self):
        """Guan and Krachi East Municipal (shared-geometry pair) must carry a Spatial_Unit_Note."""
        df = load_csv(MASTER_CSV, "Master CSV")
        for name in ("Guan", "Krachi East Municipal"):
            row = df[df["District"] == name]
            assert len(row) == 1, f"{name} missing or duplicated"
            assert row.iloc[0]["Spatial_Unit_Note"].strip() != "", f"{name} missing Spatial_Unit_Note"


class TestSpatialAutocorrelation:
    """Global Moran's I -- read from the actual results file, not a hardcoded constant."""

    def test_morans_csv_exists(self):
        df = load_csv(MORANS_CSV, "Morans_I_Results.csv")
        assert len(df) > 0, "Moran's I results CSV is empty"

    def test_morans_i_hiv_strong_positive(self):
        """HIV prevalence Moran's I must be strongly positive (> 0.50)."""
        df = load_csv(MORANS_CSV, "Morans_I_Results.csv")
        row = df[df["Variable"] == "HIV_Prev_Total_pct"].iloc[0]
        assert row["Morans_I"] > 0.50, f"Moran's I = {row['Morans_I']}; expected > 0.50"

    def test_morans_i_valid_range(self):
        df = load_csv(MORANS_CSV, "Morans_I_Results.csv")
        assert (df["Morans_I"] >= -1).all() and (df["Morans_I"] <= 1).all()

    def test_morans_i_hiv_significant(self):
        df = load_csv(MORANS_CSV, "Morans_I_Results.csv")
        row = df[df["Variable"] == "HIV_Prev_Total_pct"].iloc[0]
        assert row["Permutation_P"] <= 0.05, f"Permutation p={row['Permutation_P']}; expected <=0.05"


class TestLISAClusters:
    """LISA cluster assertions, read from the actual results file."""

    def test_lisa_csv_exists(self):
        df = load_csv(LISA_CSV, "LISA_Results.csv")
        assert len(df) > 0

    def test_lisa_valid_cluster_labels(self):
        df = load_csv(LISA_CSV, "LISA_Results.csv")
        assert set(df["LISA_Cluster_Type"].unique()) <= {"HH", "LL", "HL", "LH", "NS"}

    def test_lisa_significant_districts_present(self):
        """At least some districts must show significant LISA clustering."""
        df = load_csv(LISA_CSV, "LISA_Results.csv")
        n_sig = (df["LISA_Significant_Flag"] == 1).sum()
        assert n_sig > 0, "No significant LISA clusters found"

    def test_lisa_hh_ll_own_value_direction(self):
        """High-High districts must average higher HIV prevalence than Low-Low districts
        (own-value sanity check -- catches a sign-flip or quadrant-mislabeling bug)."""
        lisa = load_csv(LISA_CSV, "LISA_Results.csv")
        master = load_csv(MASTER_CSV, "Master CSV")
        merged = lisa.merge(master[["District", "HIV_Prev_Total_pct"]], on="District")
        hh_mean = merged.loc[merged["LISA_Cluster_Type"] == "HH", "HIV_Prev_Total_pct"].mean()
        ll_mean = merged.loc[merged["LISA_Cluster_Type"] == "LL", "HIV_Prev_Total_pct"].mean()
        assert hh_mean > ll_mean, f"HH mean ({hh_mean}) must exceed LL mean ({ll_mean})"


class TestGetisOrd:
    """Getis-Ord Gi* hotspot/coldspot assertions."""

    def test_getis_csv_exists(self):
        df = load_csv(GETIS_CSV, "Getis_Ord_Results.csv")
        assert len(df) > 0

    def test_getis_finds_both_hot_and_coldspots(self):
        """A dataset with Moran's I > 0.5 should show both hotspots and coldspots,
        not an all-non-significant result (regression guard for the pre-fix bug where
        Getis-Ord returned zero hotspots and zero coldspots across all districts)."""
        df = load_csv(GETIS_CSV, "Getis_Ord_Results.csv")
        counts = df["Hotspot_Type"].value_counts()
        assert counts.get("Hotspot", 0) > 0, "No Getis-Ord hotspots found"
        assert counts.get("Coldspot", 0) > 0, "No Getis-Ord coldspots found"


class TestRegressionModels:
    """Spatial lag, LASSO, and Random Forest assertions, read from actual results files."""

    def test_spatial_lag_csv_exists(self):
        df = load_csv(LAG_CSV, "Spatial_Lag_Regression_Results.csv")
        assert len(df) > 0

    def test_spatial_lag_rho_positive_and_significant(self):
        df = load_csv(LAG_CSV, "Spatial_Lag_Regression_Results.csv")
        row = df[df["Variable"] == "W_HIV_Prev_Total_pct"].iloc[0]
        assert row["Coefficient"] > 0, "Spatial lag rho must be positive"
        assert row["P_Value"] < 0.05, "Spatial lag rho must be statistically significant"

    def test_lasso_r2_excellent(self):
        df = load_csv(MODEL_COMP_CSV, "model_comparison.csv")
        r2 = df.loc[df["Model"] == "LASSO", "R2"].iloc[0]
        assert r2 > 0.85, f"LASSO R2 = {r2}; expected > 0.85"

    def test_rf_cv_r2_above_floor(self):
        df = load_csv(MODEL_COMP_CSV, "model_comparison.csv")
        r2 = df.loc[df["Model"] == "Random Forest (Spatial LOO-CV)", "R2"].iloc[0]
        assert r2 > 0.50, f"RF spatial CV R2 = {r2}; expected > 0.50"

    def test_lasso_csv_exists(self):
        df = load_csv(LASSO_CSV, "lasso_results.csv")
        assert len(df) > 0

    def test_rf_fold_csv_exists(self):
        df = load_csv(RF_CSV, "rf_cv_results.csv")
        assert len(df) > 0


class TestSHAPInterpretability:
    """SHAP interpretability assertions, read from the actual results file."""

    def test_shap_summary_csv_exists(self):
        df = load_csv(SHAP_SUMMARY_CSV, "shap_summary.csv")
        assert len(df) > 0

    def test_top_shap_feature_vct(self):
        """Top SHAP feature must be VCT-related."""
        df = load_csv(SHAP_SUMMARY_CSV, "shap_summary.csv")
        top = df.iloc[0]["Feature"]
        assert "vct" in top.lower(), f"Top SHAP feature should be VCT-related; got '{top}'"

    def test_shap_values_descending(self):
        """SHAP importances must be sorted in descending order."""
        df = load_csv(SHAP_SUMMARY_CSV, "shap_summary.csv")
        vals = df["Mean_Abs_SHAP"].tolist()
        assert vals == sorted(vals, reverse=True), "SHAP values must be in descending order"

    def test_shap_plots_exist(self):
        """SHAP summary, waterfall, and dependence plots must be present."""
        figures_dir = os.path.join(REPO_ROOT, "outputs", "figures")
        if not os.path.exists(figures_dir):
            pytest.skip("Figures directory not found")
        shap_files = [f for f in os.listdir(figures_dir) if "shap" in f.lower()]
        assert len(shap_files) >= 2, f"Expected >= 2 SHAP figures; found {len(shap_files)}: {shap_files}"

    def test_shap_csv_exists(self):
        df = load_csv(SHAP_CSV, "shap_values.csv")
        assert len(df) > 0, "SHAP values CSV is empty"

    def test_shap_csv_row_count_matches_districts(self):
        shap_df = load_csv(SHAP_CSV, "shap_values.csv")
        assert len(shap_df) == N_DISTRICTS, \
            f"shap_values.csv has {len(shap_df)} rows, expected {N_DISTRICTS}"


class TestRegionLevelGranularityDisclosure:
    """Guards for the region-level-outcome limitation surfaced by the 2026-07-12
    epid-council review (COUNCIL-141) -- these variables are DHS regional estimates,
    not independent district measurements, and must stay recognizably low-cardinality
    so the limitation is not silently 'fixed away' by a future data refresh without
    someone noticing the underlying granularity changed."""

    def test_hiv_prevalence_is_region_level_cardinality(self):
        df = load_csv(MASTER_CSV, "Master CSV")
        n_regions = df["Region"].nunique()
        n_unique_hiv = df["HIV_Prev_Total_pct"].nunique()
        assert n_unique_hiv <= n_regions + 2, (
            f"HIV_Prev_Total_pct now has {n_unique_hiv} unique values across "
            f"{n_regions} regions -- if this increased because district-level DHS "
            f"biomarker data is now available, update DATA_CORRECTION_NOTE.md and "
            f"README to remove the regional-granularity caveat."
        )
