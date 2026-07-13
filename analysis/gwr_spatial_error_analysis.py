"""GWR (mgwr) and Spatial Error Model (spreg.ML_Error), same predictor set as
the spatial lag model (Condom_Use_Women_pct, VCT_Women_pct,
PMTCT_Knowledge_Women_pct, Modern_Contraception_pct), for direct comparability
with Table 4. Uses the corrected 260-polygon geometry (Guan/Krachi East
population-weighted combination for the shared polygon, as in the main
pipeline)."""
import numpy as np
import pandas as pd
import geopandas as gpd
import libpysal
from libpysal.weights import Queen
import spreg
from mgwr.gwr import GWR
from mgwr.sel_bw import Sel_BW

SEED = 42
np.random.seed(SEED)

ROOT = r"C:\Users\VGhanem\Documents\Claude\Projects\Public Health & Epidemiology Research Skills\2. Spatial Epidemiology of HIV in Ghana"
SHARED = r"C:\Users\VGhanem\Documents\Claude\Projects\Public Health & Epidemiology Research Skills"
GEOJSON = SHARED + r"\Research Datasets\Ghana_New_260_District.geojson"
OUT_DIR = ROOT + r"\outputs\data"

master = pd.read_csv(ROOT + r"\outputs\data\Ghana_HIV_Spatial_Analysis_MASTER.csv")

cw = pd.read_csv(ROOT + r"\docs\district_crosswalk_261_to_260.csv")
cw.loc[cw['master_sheet_district'] == 'Awutu Senya West', ['geojson_district', 'match_method']] = ['AWUTU SENYA', 'x']
cw.loc[cw['master_sheet_district'] == 'Sagnarigu Municipal', ['geojson_district', 'match_method']] = ['SAGNERIGU', 'x']
cw_nongap = cw[cw['match_method'] != 'structural_gap']

gdf_geo = gpd.read_file(GEOJSON)[['DISTRICT', 'REGION', 'geometry']]
gdf_geo['DISTRICT'] = gdf_geo['DISTRICT'].str.strip()

gdf = gdf_geo.merge(cw_nongap[['master_sheet_district', 'geojson_district']],
                     left_on='DISTRICT', right_on='geojson_district', how='left')
gdf = gdf.merge(master, left_on='master_sheet_district', right_on='District', how='left')

# Combine Guan + Krachi East Municipal by population-weighted mean (same as main pipeline)
guan = master[master['District'] == 'Guan'].iloc[0]
krachi = master[master['District'] == 'Krachi East Municipal'].iloc[0]
numeric_cols = master.select_dtypes(include=[np.number]).columns.tolist()
idx = gdf[gdf['DISTRICT'] == 'KRACHI EAST MUNICIPAL'].index
w1, w2 = krachi['Total_Pop'], guan['Total_Pop']
for c in numeric_cols:
    gdf.loc[idx, c] = (krachi[c] * w1 + guan[c] * w2) / (w1 + w2) if c != 'Total_Pop' else w1 + w2

assert gdf['District'].notna().all() and len(gdf) == 260

gdf = gdf.set_geometry('geometry').set_crs('EPSG:4326').to_crs('EPSG:32630').reset_index(drop=True)

predictors = ['Condom_Use_Women_pct', 'VCT_Women_pct', 'PMTCT_Knowledge_Women_pct', 'Modern_Contraception_pct']
y = gdf[['HIV_Prev_Total_pct']].values
X = gdf[predictors].values
coords = list(zip(gdf.geometry.centroid.x, gdf.geometry.centroid.y))

print("=" * 70)
print("SPATIAL ERROR MODEL (ML estimation, Queen contiguity)")
print("=" * 70)
w_queen = Queen.from_dataframe(gdf, use_index=False)
w_queen.transform = 'r'
err_model = spreg.ML_Error(y, X, w=w_queen, name_y='HIV_Prev_Total_pct', name_x=predictors, name_w='queen')
print(err_model.summary)

print("\n" + "=" * 70)
print("GWR ATTEMPT 1: DHS regional predictors (same as spatial lag/error)")
print("=" * 70)
X_gwr = X  # mgwr adds intercept internally
gwr_regional_failed = False
try:
    selector = Sel_BW(coords, y, X_gwr)
    bw = selector.search(bw_min=40)
    print(f"Optimal (adaptive) bandwidth: {bw:.1f} nearest neighbours")
    gwr_model = GWR(coords, y, X_gwr, bw)
    gwr_results = gwr_model.fit()
    print(f"GWR R2 (global): {gwr_results.R2:.4f}, AICc: {gwr_results.aicc:.2f}")
except np.linalg.LinAlgError as e:
    gwr_regional_failed = True
    print(f"GWR FAILED with DHS-regional predictors: {e}")
    print("This is expected and diagnostically meaningful: local design matrices become singular "
          "because condom use/VCT/PMTCT knowledge/modern contraception are constant within each "
          "DHS region, so small local neighbourhoods contain zero within-window predictor variance.")

print("\n" + "=" * 70)
print("GWR ATTEMPT 2: district-level-only predictors (genuine local variation)")
print("=" * 70)
district_predictors = ['Poverty_Incidence_pct', 'Illiteracy_Rate_pct', 'Uninsured_Rate_pct',
                        'Unemployment_Rate_pct', 'Youth_Dependency_Ratio', 'Latitude', 'Longitude']
X_district = gdf[district_predictors].values
selector_d = Sel_BW(coords, y, X_district)
bw_d = selector_d.search()
print(f"Optimal (adaptive) bandwidth: {bw_d:.1f} nearest neighbours")
gwr_model_d = GWR(coords, y, X_district, bw_d)
gwr_results = gwr_model_d.fit()
print(f"GWR R2 (global): {gwr_results.R2:.4f}")
print(f"GWR AICc: {gwr_results.aicc:.2f}")
print(f"Adjusted alpha (multiple testing): {gwr_results.adj_alpha}")
coef_names_for_summary = ['Intercept'] + district_predictors
bw = bw_d

# Compare to global OLS AICc for the same (district-level) predictors
import statsmodels.api as sm
X_ols = sm.add_constant(X_district)
ols_model = sm.OLS(y, X_ols).fit()
print(f"\nGlobal OLS R2 (same district-level predictors): {ols_model.rsquared:.4f}, AICc (approx): {ols_model.aic:.2f}")

local_r2 = gwr_results.localR2.flatten()
print(f"\nLocal R2 range: {local_r2.min():.4f} to {local_r2.max():.4f}")
print(f"Local R2 mean (SD): {local_r2.mean():.4f} ({local_r2.std():.4f})")

# Coefficient variability per predictor (local coefficient SD relative to mean |coef|)
coef_names = coef_names_for_summary
params = gwr_results.params  # n x k
for i, name in enumerate(coef_names):
    col = params[:, i]
    print(f"{name}: local coef mean={col.mean():.4f}, SD={col.std():.4f}, "
          f"range=[{col.min():.4f}, {col.max():.4f}]")

gdf['gwr_local_r2'] = local_r2
gdf[['District', 'Region', 'gwr_local_r2']].to_csv(OUT_DIR + r"\gwr_local_r2.csv", index=False)

err_summary = pd.DataFrame({
    'Variable': ['Constant'] + predictors,
    'Coefficient': list(err_model.betas.flatten()[:-1]),
    'Std_Error': list(err_model.std_err.flatten()[:-1]),
})
err_summary['Z_Statistic'] = err_summary['Coefficient'] / err_summary['Std_Error']
from scipy import stats as sstats
err_summary['P_Value'] = 2 * (1 - sstats.norm.cdf(np.abs(err_summary['Z_Statistic'])))
err_summary.loc[len(err_summary)] = ['lambda (spatial error)', err_model.betas.flatten()[-1],
                                       err_model.std_err.flatten()[-1],
                                       err_model.betas.flatten()[-1] / err_model.std_err.flatten()[-1],
                                       2 * (1 - sstats.norm.cdf(abs(err_model.betas.flatten()[-1] / err_model.std_err.flatten()[-1])))]
err_summary.to_csv(OUT_DIR + r"\spatial_error_model_results.csv", index=False)
print(f"\nSpatial Error pseudo-R2: {err_model.pr2:.4f}")

gwr_summary = pd.DataFrame({
    'Predictor': coef_names,
    'Mean_Local_Coef': params.mean(axis=0),
    'SD_Local_Coef': params.std(axis=0),
    'Min_Local_Coef': params.min(axis=0),
    'Max_Local_Coef': params.max(axis=0),
})
gwr_summary.to_csv(OUT_DIR + r"\gwr_coefficient_summary.csv", index=False)

with open(OUT_DIR + r"\gwr_spatial_error_metadata.txt", 'w') as f:
    f.write(f"GWR (DHS-regional predictors) singular-matrix failure: {gwr_regional_failed}\n")
    f.write("Reason: condom use/VCT/PMTCT knowledge/modern contraception are constant within each "
            "DHS region, so small local GWR neighbourhoods contain zero within-window predictor "
            "variance, making the local design matrix singular.\n\n")
    f.write(f"GWR (district-level predictors) bandwidth (adaptive, nearest neighbours): {bw:.1f}\n")
    f.write(f"GWR global R2: {gwr_results.R2:.4f}\n")
    f.write(f"GWR AICc: {gwr_results.aicc:.2f}\n")
    f.write(f"Global OLS R2 (same district-level predictors): {ols_model.rsquared:.4f}\n")
    f.write(f"Global OLS AIC: {ols_model.aic:.2f}\n")
    f.write(f"GWR local R2 range: {local_r2.min():.4f} to {local_r2.max():.4f}\n")
    f.write(f"GWR local R2 mean (SD): {local_r2.mean():.4f} ({local_r2.std():.4f})\n")
    f.write(f"Spatial Error Model (DHS-regional predictors) pseudo-R2: {err_model.pr2:.4f}\n")
    f.write(f"Spatial Error Model lambda: {err_model.betas.flatten()[-1]:.4f}\n")

print("\nSaved: gwr_local_r2.csv, gwr_coefficient_summary.csv, spatial_error_model_results.csv, gwr_spatial_error_metadata.txt")
