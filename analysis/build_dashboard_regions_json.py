import json
import pandas as pd

D = r"C:\Users\VGhanem\Documents\Claude\Projects\Public Health & Epidemiology Research Skills\2. Spatial Epidemiology of HIV in Ghana"

lisa = pd.read_csv(D + r"\outputs\data\LISA_Results.csv")
mc = pd.read_csv(D + r"\outputs\data\Ghana_HIV_Spatial_Analysis_MASTER.csv")
cw = pd.read_csv(D + r"\docs\district_crosswalk_261_to_260.csv")

merged = mc[["District", "Region", "HIV_Prev_Total_pct", "Poverty_Incidence_pct"]].merge(
    lisa[["District", "LISA_Cluster_Type"]], on="District", how="left"
)
merged["LISA_Cluster_Type"] = merged["LISA_Cluster_Type"].fillna("NS")

merged = merged.merge(
    cw[["master_sheet_district", "geojson_district"]],
    left_on="District", right_on="master_sheet_district", how="left"
)

# Two crosswalk notes are stale relative to the actual geojson feature list:
# - "Awutu Senya West" has no own polygon; crosswalk correctly notes it is absorbed
#   into the pre-2012 parent "AWUTU SENYA" polygon, but leaves geojson_district blank.
# - "Sagnarigu Municipal" crosswalk note claims absorption into "TAMALE METROPOLITAN",
#   but the geojson actually carries a standalone "SAGNERIGU" polygon (verified via
#   live inspection of the rendered map's feature list) -- use that directly instead.
MANUAL_FIX = {"Awutu Senya West": "AWUTU SENYA", "Sagnarigu Municipal": "SAGNERIGU"}
for district, geoname in MANUAL_FIX.items():
    merged.loc[merged["District"] == district, "geojson_district"] = geoname

missing = merged[merged["geojson_district"].isna()]
print("districts with no geojson_district (excluded from map, kept in KPI count):")
print(missing[["District", "Region"]].to_string())

def shortname(name):
    n = name.title()
    for suf in [" Municipal", " Metropolitan", " District"]:
        if n.endswith(suf):
            n = n[: -len(suf)]
    return n

out = []
skipped = 0
for _, row in merged.iterrows():
    geoname = row["geojson_district"]
    if pd.isna(geoname):
        skipped += 1
        continue
    out.append({
        "name": geoname,
        "short": shortname(row["District"]),
        "v": round(float(row["HIV_Prev_Total_pct"]), 2),
        "lisa": row["LISA_Cluster_Type"],
        "x": round(float(row["Poverty_Incidence_pct"]), 2) if pd.notna(row["Poverty_Incidence_pct"]) else None,
    })

print("total analytical districts:", len(merged), "| mapped (geojson-matched):", len(out), "| skipped (no polygon):", skipped)

cluster_counts = {}
for r in out:
    cluster_counts[r["lisa"]] = cluster_counts.get(r["lisa"], 0) + 1
print("cluster counts (mapped only):", cluster_counts)

TMP = r"C:\Users\VGhanem\AppData\Local\Temp"
with open(TMP + r"\hiv-spatial_regions.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print("wrote", len(out), "entries")
