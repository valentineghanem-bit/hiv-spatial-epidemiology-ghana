"""
Ghana HIV Spatial Epidemiology - Spatial/ML Analysis Pipeline
================================================================
Computes Global Moran's I, LISA, Bivariate LISA, Getis-Ord Gi*, Spatial Lag
Regression, LASSO, and Random Forest/SHAP for all 261 census districts.

Attribute data (261 census districts) is joined to the canonical 260-polygon
GSS boundary file via docs/district_crosswalk_261_to_260.csv. Guan (created
2018 from Krachi East Municipal; no distinct 2023 boundary polygon exists)
shares its parent polygon's geometry; the two districts' values are combined
by Total_Pop-weighted mean for geometry-dependent statistics only. All 261
districts are retained in the Master CSV with their own covariate values.

Usage:
    python analysis/spatial_analysis_pipeline.py

Run from the repo root, or with paths adjusted for your working directory.
Fixed seed = 42 throughout for reproducibility.
"""
import json
import os
import numpy as np
import pandas as pd
import geopandas as gpd
import libpysal
from libpysal.weights import Queen, Rook, KNN
import esda
from spreg import ML_Lag
from scipy import stats as sstats
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import shap
from collections import Counter

SEED = 42
np.random.seed(SEED)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CSV = os.path.join(ROOT, "outputs", "data", "Ghana_HIV_Analysis_Dataset_260districts.csv")
CROSSWALK_CSV = os.path.join(ROOT, "docs", "district_crosswalk_261_to_260.csv")
GEOJSON = os.path.join(ROOT, "data", "raw", "Ghana_New_260_District.geojson")
OUT_DIR = os.path.join(ROOT, "outputs", "data")

LASSO_FEATURES = ['Poverty_Incidence_pct', 'Illiteracy_Rate_pct', 'Uninsured_Rate_pct',
                   'Unemployment_Rate_pct', 'Youth_Dependency_Ratio', 'Latitude', 'Longitude',
                   'Condom_Use_Women_pct', 'VCT_Women_pct', 'HIV_Awareness_Women_pct',
                   'PMTCT_Knowledge_Women_pct', 'No_Insurance_Women_pct', 'Literacy_Women_pct',
                   'Edu_Secondary_Women_pct', 'No_Education_Women_pct', 'Modern_Contraception_pct',
                   'Adolescent_Fertility_Rate', 'Wife_Beating_Accept_pct', 'Unmet_FP_Need_pct']
LAG_PREDICTORS = ['Condom_Use_Women_pct', 'VCT_Women_pct', 'PMTCT_Knowledge_Women_pct', 'Modern_Contraception_pct']
MORANS_VARS = ['HIV_Prev_Total_pct', 'HIV_Prev_Women_pct', 'Poverty_Incidence_pct',
               'Illiteracy_Rate_pct', 'VCT_Women_pct', 'Condom_Use_Women_pct']
BIV_PAIRS = ['Poverty_Incidence_pct', 'Illiteracy_Rate_pct', 'Condom_Use_Women_pct', 'VCT_Women_pct']


def load_and_join():
    df_base = pd.read_csv(BASE_CSV)
    assert len(df_base) == 261, f"Expected 261 base rows, got {len(df_base)}"

    cw = pd.read_csv(CROSSWALK_CSV)
    assert len(cw) == 261
    # This project's 2023 GSS boundary file carries standalone polygons for these
    # two districts (AWUTU SENYA, SAGNERIGU) that the shared crosswalk's authors
    # had marked as fully absorbed elsewhere -- verified against the actual
    # geometry file below. Guan remains the one genuine structural gap.
    cw.loc[cw['master_sheet_district'] == 'Awutu Senya West',
           ['geojson_district', 'match_method']] = ['AWUTU SENYA', 'manual_resolved_p2_audit']
    cw.loc[cw['master_sheet_district'] == 'Sagnarigu Municipal',
           ['geojson_district', 'match_method']] = ['SAGNERIGU', 'manual_resolved_p2_audit']
    gap_rows = cw[cw['match_method'] == 'structural_gap']
    assert len(gap_rows) == 1 and gap_rows.iloc[0]['master_sheet_district'] == 'Guan'

    gdf_geo = gpd.read_file(GEOJSON)[['DISTRICT', 'REGION', 'geometry']]
    gdf_geo['DISTRICT'] = gdf_geo['DISTRICT'].str.strip()
    assert len(gdf_geo) == 260

    df = df_base.merge(cw[['master_sheet_district', 'geojson_district', 'match_method', 'note']],
                        left_on='District', right_on='master_sheet_district', how='left')
    guan_row = df[df['District'] == 'Guan'].iloc[0]
    krachi_row = df[df['District'] == 'Krachi East Municipal'].iloc[0]

    df_nongap = df[df['match_method'] != 'structural_gap'].copy()
    gdf = gdf_geo.merge(df_nongap, left_on='DISTRICT', right_on='geojson_district', how='left')
    assert gdf['District'].isna().sum() == 0 and len(gdf) == 260

    # Population-weighted combination of Guan + Krachi East Municipal for the
    # shared polygon, used only for geometry-dependent statistics below.
    numeric_cols = df_base.select_dtypes(include=[np.number]).columns.tolist()
    w1, w2 = krachi_row['Total_Pop'], guan_row['Total_Pop']
    idx = gdf[gdf['DISTRICT'] == 'KRACHI EAST MUNICIPAL'].index
    for c in numeric_cols:
        gdf.loc[idx, c] = (krachi_row[c] * w1 + guan_row[c] * w2) / (w1 + w2) if c != 'Total_Pop' else w1 + w2

    gdf = gdf.set_geometry('geometry').set_crs('EPSG:4326').to_crs('EPSG:32630').reset_index(drop=True)
    return df, gdf


def build_weights(gdf):
    w_rook = Rook.from_dataframe(gdf, use_index=False)
    w_rook.transform = 'r'
    w_knn4 = KNN.from_dataframe(gdf, k=4, use_index=False)
    w_knn4.transform = 'r'
    w_queen = Queen.from_dataframe(gdf, use_index=False)
    w_queen.transform = 'r'
    return w_rook, w_knn4, w_queen


def run_spatial_stats(gdf, w_rook, w_knn4, w_queen):
    morans_results = []
    for v in MORANS_VARS:
        mi = esda.Moran(gdf[v].values, w_knn4, permutations=999)
        morans_results.append({'Variable': v, 'Morans_I': mi.I, 'Expected_I': mi.EI,
                                'Z_Score': mi.z_norm, 'P_Value': mi.p_norm,
                                'Permutation_P': mi.p_sim, 'N': len(gdf)})
    df_morans = pd.DataFrame(morans_results)

    y_hiv = gdf['HIV_Prev_Total_pct'].values
    lisa = esda.Moran_Local(y_hiv, w_rook, permutations=999, seed=SEED)
    sig = lisa.p_sim < 0.05
    quad_labels = {1: 'HH', 2: 'LH', 3: 'LL', 4: 'HL'}
    cluster_type = np.array([quad_labels[q] if s else 'NS' for q, s in zip(lisa.q, sig)])
    gdf['LISA_Local_Morans_I'] = lisa.Is
    gdf['LISA_P_Value'] = lisa.p_sim
    gdf['LISA_Significant_Flag'] = sig.astype(int)
    gdf['LISA_Cluster_Type'] = cluster_type
    lisa_counts = Counter(cluster_type)

    biv_results, biv_local_frames = {}, []
    for v in BIV_PAIRS:
        bglobal = esda.Moran_BV(gdf['HIV_Prev_Total_pct'].values, gdf[v].values, w_rook, permutations=999)
        blocal = esda.Moran_Local_BV(gdf['HIV_Prev_Total_pct'].values, gdf[v].values, w_rook,
                                      permutations=999, seed=SEED)
        bsig = int((blocal.p_sim < 0.05).sum())
        biv_results[v] = {'Global_I': float(bglobal.I), 'significant_locations': bsig}
        biv_local_frames.append(pd.DataFrame({
            'District': gdf['District'], 'Region': gdf['Region'], 'Variable_2': v,
            'Local_Bivariate_I': blocal.Is, 'P_Value': blocal.p_sim,
            'Significant': (blocal.p_sim < 0.05).astype(int)}))
    df_biv_local = pd.concat(biv_local_frames, ignore_index=True)

    gi = esda.G_Local(y_hiv, w_knn4, star=True, permutations=999, seed=SEED)
    gi_sig = gi.p_sim < 0.05
    hotspot, coldspot = gi_sig & (gi.Zs > 0), gi_sig & (gi.Zs < 0)
    gdf['GetisOrd_Class'] = np.where(hotspot, 'Hotspot', np.where(coldspot, 'Coldspot', 'Not Significant'))
    df_getis = pd.DataFrame({'District': gdf['District'], 'HIV_Prev_Total_pct': gdf['HIV_Prev_Total_pct'],
                              'G_Star_Z_Score': gi.Zs, 'P_Value': gi.p_sim, 'Hotspot_Type': gdf['GetisOrd_Class']})

    Y, X = gdf[['HIV_Prev_Total_pct']].values, gdf[LAG_PREDICTORS].values
    lag_model = ML_Lag(Y, X, w=w_queen, name_y='HIV_Prev_Total_pct', name_x=LAG_PREDICTORS, name_w='queen')

    return {
        'df_morans': df_morans, 'lisa_counts': lisa_counts, 'lisa_sig_n': int(sig.sum()),
        'biv_results': biv_results, 'df_biv_local': df_biv_local,
        'gi_hotspot': int(hotspot.sum()), 'gi_coldspot': int(coldspot.sum()),
        'gi_ns': int((~gi_sig).sum()), 'df_getis': df_getis, 'lag_model': lag_model,
    }


def run_ml(df):
    Xml = df[LASSO_FEATURES].values
    yml = df['HIV_Prev_Total_pct'].values
    scaler = StandardScaler()
    Xml_scaled = scaler.fit_transform(Xml)
    lasso = LassoCV(cv=10, random_state=SEED, max_iter=10000).fit(Xml_scaled, yml)
    pred = lasso.predict(Xml_scaled)
    lasso_coefs = pd.DataFrame({'Feature': LASSO_FEATURES, 'Coefficient': lasso.coef_})
    lasso_coefs['Abs_Coefficient'] = lasso_coefs['Coefficient'].abs()
    lasso_coefs = lasso_coefs.sort_values('Abs_Coefficient', ascending=False).reset_index(drop=True)
    lasso_metrics = {'alpha': lasso.alpha_, 'r2': r2_score(yml, pred),
                      'rmse': np.sqrt(mean_squared_error(yml, pred)), 'mae': mean_absolute_error(yml, pred),
                      'n_selected': int((lasso_coefs['Coefficient'] != 0).sum())}

    regions = df['Region'].unique()
    fold_results, oof_pred = [], np.zeros(len(df))
    for region in regions:
        train_mask = (df['Region'] != region).values
        test_mask = (df['Region'] == region).values
        rf_fold = RandomForestRegressor(n_estimators=500, random_state=SEED, n_jobs=-1).fit(
            df.loc[train_mask, LASSO_FEATURES], df.loc[train_mask, 'HIV_Prev_Total_pct'])
        pred_fold = rf_fold.predict(df.loc[test_mask, LASSO_FEATURES])
        oof_pred[test_mask] = pred_fold
        yte = df.loc[test_mask, 'HIV_Prev_Total_pct']
        fold_results.append({'Region_Left_Out': region, 'N_Test_Districts': int(test_mask.sum()),
                              'R2': r2_score(yte, pred_fold) if test_mask.sum() > 1 else np.nan,
                              'RMSE': np.sqrt(mean_squared_error(yte, pred_fold)),
                              'MAE': mean_absolute_error(yte, pred_fold)})
    df_rf_folds = pd.DataFrame(fold_results)
    rf_metrics = {'r2': r2_score(df['HIV_Prev_Total_pct'], oof_pred),
                  'rmse': np.sqrt(mean_squared_error(df['HIV_Prev_Total_pct'], oof_pred)),
                  'mae': mean_absolute_error(df['HIV_Prev_Total_pct'], oof_pred)}

    rf_full = RandomForestRegressor(n_estimators=500, random_state=SEED, n_jobs=-1).fit(
        df[LASSO_FEATURES], df['HIV_Prev_Total_pct'])
    explainer = shap.TreeExplainer(rf_full)
    shap_values = explainer.shap_values(df[LASSO_FEATURES])
    mean_abs_shap = pd.DataFrame({'Feature': LASSO_FEATURES,
                                   'Mean_Abs_SHAP': np.abs(shap_values).mean(axis=0)})
    mean_abs_shap = mean_abs_shap.sort_values('Mean_Abs_SHAP', ascending=False).reset_index(drop=True)
    df_shap_full = pd.DataFrame(shap_values, columns=LASSO_FEATURES)
    df_shap_full['HIV_Prev_Total_pct_actual'] = df['HIV_Prev_Total_pct'].values
    df_shap_full['District'] = df['District'].values

    return {'lasso_coefs': lasso_coefs, 'lasso_metrics': lasso_metrics, 'df_rf_folds': df_rf_folds,
            'rf_metrics': rf_metrics, 'mean_abs_shap': mean_abs_shap, 'df_shap_full': df_shap_full,
            'n_regions': len(regions)}


def build_master(df, gdf):
    lisa_cols = ['LISA_Local_Morans_I', 'LISA_P_Value', 'LISA_Significant_Flag', 'LISA_Cluster_Type']
    gap_vals = gdf.loc[gdf['DISTRICT'] == 'KRACHI EAST MUNICIPAL', lisa_cols].iloc[0]

    df_master = df.drop(columns=['master_sheet_district', 'geojson_district', 'match_method', 'note']).copy()
    df_master = df_master.merge(gdf[['District'] + lisa_cols], on='District', how='left')
    guan_idx = df_master[df_master['District'] == 'Guan'].index
    krachi_idx = df_master[df_master['District'] == 'Krachi East Municipal'].index
    for c in lisa_cols:
        df_master.loc[guan_idx, c] = gap_vals[c]
    df_master['Spatial_Unit_Note'] = ''
    df_master.loc[guan_idx, 'Spatial_Unit_Note'] = (
        'Shares GSS 260-polygon geometry with Krachi East Municipal (Guan created 2018 from '
        'Krachi East; no distinct 2023 boundary polygon exists). LISA/Getis-Ord/spatial-lag '
        'statistics reflect the combined population-weighted spatial unit; HIV/behavioural/'
        'socioeconomic covariates above remain Guan-specific.')
    df_master.loc[krachi_idx, 'Spatial_Unit_Note'] = (
        'Shares GSS 260-polygon geometry with Guan (see Guan note). LISA/Getis-Ord/spatial-lag '
        'statistics reflect the combined population-weighted spatial unit.')

    df_master['Data_Source_HIV_Prevalence'] = "Ghana DHS 2014 — hiv-prevalence_subnational_gha.csv (regional level, mapped to 261 districts)"
    df_master['Data_Source_Behavioural'] = "Ghana DHS 2022 — hiv-behavior/knowledge/counseling/attitudes/fp2020_subnational_gha.csv (regional level)"
    df_master['Data_Source_Socioeconomic'] = "Ghana Population & Housing Census 2021 — Master Sheet.xlsx (district level)"
    df_master['Data_Source_Insurance'] = "Ghana DHS 2022 — health-insurance_subnational_gha.csv (regional level)"
    df_master['Data_Source_Education'] = "Ghana DHS 2022 — literacy/select-education-indicators_subnational_gha.csv (regional level)"
    df_master['Data_Source_Spatial_Boundaries'] = (
        "Ghana Statistical Service — Ghana_New_260_District.geojson, joined via "
        "docs/district_crosswalk_261_to_260.csv (261 census districts -> 260 unique polygons; "
        "Guan shares Krachi East Municipal's polygon)")

    assert len(df_master) == 261 and df_master['District'].is_unique
    return df_master


def main():
    df, gdf = load_and_join()
    w_rook, w_knn4, w_queen = build_weights(gdf)
    spatial = run_spatial_stats(gdf, w_rook, w_knn4, w_queen)
    ml = run_ml(df)
    df_master = build_master(df, gdf)

    df_master.to_csv(os.path.join(OUT_DIR, "Ghana_HIV_Spatial_Analysis_MASTER.csv"), index=False)
    spatial['df_morans'].to_csv(os.path.join(OUT_DIR, "Morans_I_Results.csv"), index=False)
    gdf[['District', 'Region', 'LISA_Local_Morans_I', 'LISA_P_Value',
         'LISA_Significant_Flag', 'LISA_Cluster_Type']].to_csv(
        os.path.join(OUT_DIR, "LISA_Results.csv"), index=False)
    spatial['df_getis'].to_csv(os.path.join(OUT_DIR, "Getis_Ord_Results.csv"), index=False)
    spatial['df_biv_local'].to_csv(os.path.join(OUT_DIR, "Bivariate_LISA_Local_Results.csv"), index=False)
    pd.DataFrame([{'Variable_1': 'HIV_Prev_Total_pct', 'Variable_2': k,
                    'Global_Bivariate_Morans_I': v['Global_I'],
                    'Significant_Locations': v['significant_locations']}
                  for k, v in spatial['biv_results'].items()]).to_csv(
        os.path.join(OUT_DIR, "Bivariate_LISA_Results.csv"), index=False)

    lag_model = spatial['lag_model']
    lag_summary = pd.DataFrame({
        'Variable': ['Constant'] + LAG_PREDICTORS + ['W_HIV_Prev_Total_pct'],
        'Coefficient': list(lag_model.betas.flatten()),
        'Std_Error': list(lag_model.std_err.flatten())})
    lag_summary['T_Statistic'] = lag_summary['Coefficient'] / lag_summary['Std_Error']
    lag_summary['P_Value'] = 2 * (1 - sstats.norm.cdf(np.abs(lag_summary['T_Statistic'])))
    lag_summary.to_csv(os.path.join(OUT_DIR, "Spatial_Lag_Regression_Results.csv"), index=False)

    ml['lasso_coefs'].to_csv(os.path.join(OUT_DIR, "lasso_results.csv"), index=False)
    ml['df_rf_folds'].to_csv(os.path.join(OUT_DIR, "rf_cv_results.csv"), index=False)
    ml['mean_abs_shap'].to_csv(os.path.join(OUT_DIR, "shap_summary.csv"), index=False)
    ml['df_shap_full'].to_csv(os.path.join(OUT_DIR, "shap_values.csv"), index=False)
    pd.DataFrame([
        {'Model': 'LASSO', 'R2': round(ml['lasso_metrics']['r2'], 4),
         'RMSE': round(ml['lasso_metrics']['rmse'], 4), 'MAE': round(ml['lasso_metrics']['mae'], 4),
         'Num_Features_Selected': ml['lasso_metrics']['n_selected']},
        {'Model': 'Random Forest (Spatial LOO-CV)', 'R2': round(ml['rf_metrics']['r2'], 4),
         'RMSE': round(ml['rf_metrics']['rmse'], 4), 'MAE': round(ml['rf_metrics']['mae'], 4),
         'Num_Features_Selected': len(LASSO_FEATURES)},
    ]).to_csv(os.path.join(OUT_DIR, "model_comparison.csv"), index=False)

    spatial_json = {
        "analysis_date": "2026-07-12", "seed": SEED,
        "dataset_info": {"total_districts_census": 261, "total_unique_polygons": 260,
                          "total_variables": int(df_master.shape[1]), "crs": "EPSG:32630",
                          "note": "Guan shares Krachi East Municipal's polygon; spatial statistics for "
                                  "both reflect the combined population-weighted unit."},
        "morans_i_analysis": {"description": "Global spatial autocorrelation test (KNN k=4)",
                               "results": spatial['df_morans'].set_index('Variable').to_dict(orient='index')},
        "lisa_analysis": {"description": "Local spatial autocorrelation (Rook contiguity, 999 permutations, seed=42)",
                           "variable": "HIV_Prev_Total_pct",
                           "cluster_counts": {k: int(v) for k, v in spatial['lisa_counts'].items()},
                           "significant_districts": spatial['lisa_sig_n']},
        "bivariate_lisa_analysis": {"description": "Bivariate local spatial association (Rook, 999 perms)",
                                     "results": spatial['biv_results']},
        "getis_ord_analysis": {"description": "Hotspot/Coldspot analysis (Getis-Ord Gi*, KNN k=4)",
                                "classifications": {"Hotspot": spatial['gi_hotspot'],
                                                     "Coldspot": spatial['gi_coldspot'],
                                                     "Not Significant": spatial['gi_ns']}},
        "spatial_lag_regression": {"description": "Spatial Lag Model (ML estimation, Queen weights)",
                                    "dependent_variable": "HIV_Prev_Total_pct",
                                    "independent_variables": LAG_PREDICTORS,
                                    "rho": float(lag_model.betas.flatten()[-1]),
                                    "pseudo_r_squared": float(lag_model.pr2)},
    }
    with open(os.path.join(OUT_DIR, "spatial_analysis_results.json"), "w") as f:
        json.dump(spatial_json, f, indent=1, default=str)

    ml_json = {
        "Dataset": {"N_Districts": 261, "N_Predictors": len(LASSO_FEATURES), "N_Regions": ml['n_regions'],
                    "Outcome_Variable": "HIV_Prev_Total_pct",
                    "Outcome_Mean": float(df['HIV_Prev_Total_pct'].mean()),
                    "Outcome_Std": float(df['HIV_Prev_Total_pct'].std())},
        "LASSO_Results": {"Optimal_Alpha": ml['lasso_metrics']['alpha'],
                           "N_Selected_Features": ml['lasso_metrics']['n_selected'],
                           "R2": round(ml['lasso_metrics']['r2'], 4), "RMSE": round(ml['lasso_metrics']['rmse'], 4),
                           "MAE": round(ml['lasso_metrics']['mae'], 4),
                           "Top_5_Features": ml['lasso_coefs'].head(5).to_dict(orient='records')},
        "Random_Forest_Spatial_LOOCV": {"N_Folds": ml['n_regions'], "N_Trees": 500,
                                         "CV_Strategy": "Leave-one-region-out",
                                         "Overall_R2_Aggregated": round(ml['rf_metrics']['r2'], 4),
                                         "Overall_RMSE_Aggregated": round(ml['rf_metrics']['rmse'], 4),
                                         "Overall_MAE_Aggregated": round(ml['rf_metrics']['mae'], 4)},
        "SHAP_Feature_Importance": {"Top_10_Features": ml['mean_abs_shap'].head(10).to_dict(orient='records')},
    }
    with open(os.path.join(OUT_DIR, "ml_analysis_results.json"), "w") as f:
        json.dump(ml_json, f, indent=1, default=str)

    print("Pipeline complete. Master CSV:", df_master.shape)
    print("LISA cluster counts:", dict(spatial['lisa_counts']))
    print("Getis-Ord:", spatial['gi_hotspot'], "hotspots,", spatial['gi_coldspot'], "coldspots")


if __name__ == '__main__':
    main()
