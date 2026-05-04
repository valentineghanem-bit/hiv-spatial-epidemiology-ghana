"""
Ghana HIV Spatial Epidemiology - Master Dataset Builder
========================================================

Builds the replicable final CSV for journal submission.
Combines base dataset (260 core districts) with spatial analysis results (LISA) and data source attribution.

Core reference: 260 districts with complete spatial and epidemiological data.

Usage:
 python build_master_dataset.py

Output:
 Ghana_HIV_Spatial_Analysis_MASTER.csv (260 districts x 48 columns)
"""

import pandas as pd
import numpy as np
import sys

def load_source_data():
 """Load all input datasets."""
 print("Loading source datasets...")

 df_base = pd.read_csv('Ghana_HIV_Analysis_Dataset_260districts.csv')
 df_lisa = pd.read_csv('LISA_Results.csv')
 df_morans = pd.read_csv('Morans_I_Results.csv')
 df_spatial_lag = pd.read_csv('Spatial_Lag_Regression_Results.csv')

 print(f" Base dataset: {df_base.shape} (includes 261 administrative divisions)")
 print(f" LISA results: {df_lisa.shape} (260 core districts)")
 print(f" Moran's I: {df_morans.shape}")
 print(f" Spatial Lag Regression: {df_spatial_lag.shape}")

 return df_base, df_lisa, df_morans, df_spatial_lag

def filter_to_260_core(df_base, df_lisa):
 """Filter base dataset to 260 core districts that have LISA results."""
 print("\nFiltering to 260-district core reference...")

 # Get the 260 districts from LISA
 core_districts = set(df_lisa['District'])

 # Filter base to only these districts
 df_260 = df_base[df_base['District'].isin(core_districts)].copy()

 # Reset index
 df_260.reset_index(drop=True, inplace=True)

 excluded = len(df_base) - len(df_260)
 print(f" Base dataset: {len(df_base)} districts")
 print(f" Core reference: {len(df_260)} districts")
 print(f" Excluded (not in spatial analysis): {excluded} districts")

 return df_260

def merge_lisa_results(df_base, df_lisa):
 """Merge LISA cluster analysis results by district name."""
 print("\nMerging LISA spatial cluster results...")

 # Merge by exact district name match
 df_merged = df_base.merge(
 df_lisa[['District', 'Local_Morans_I', 'P_Value', 'Significant', 'Cluster_Type']],
 on='District',
 how='left'
 )

 # Rename LISA columns for clarity
 df_merged.rename(columns={
 'Local_Morans_I': 'LISA_Local_Morans_I',
 'P_Value': 'LISA_P_Value',
 'Significant': 'LISA_Significant_Flag',
 'Cluster_Type': 'LISA_Cluster_Type'
 }, inplace=True)

 merged_successfully = df_merged['LISA_Local_Morans_I'].notna().sum()
 print(f" Districts with LISA results: {merged_successfully}/{len(df_merged)}")

 return df_merged

def add_data_source_attribution(df):
 """Add explicit data source attribution columns as literal strings."""
 print("\nAdding data source attribution columns...")

 # Add data source columns for all rows
 df['Data_Source_HIV_Prevalence'] = "Ghana DHS 2014 — hiv-prevalence_subnational_gha.csv (regional level, mapped to 260 districts)"
 df['Data_Source_Behavioural'] = "Ghana DHS 2022 — hiv-behavior/knowledge/counseling/attitudes/fp2020_subnational_gha.csv (regional level)"
 df['Data_Source_Socioeconomic'] = "Ghana Population & Housing Census 2021 — Master Sheet.xlsx (district level)"
 df['Data_Source_Insurance'] = "Ghana DHS 2022 — health-insurance_subnational_gha.csv (regional level)"
 df['Data_Source_Education'] = "Ghana DHS 2022 — literacy/select-education-indicators_subnational_gha.csv (regional level)"
 df['Data_Source_Spatial_Boundaries'] = "Ghana Statistical Service — Ghana_New_260_District.geojson"

 print(f" Attribution columns added: 6")

 return df

def reorder_columns(df):
 """Reorder columns to logical grouping: IDs, spatial, HIV, behavioural, socioeconomic, derived, spatial analysis, sources."""
 print("\nReordering columns for logical grouping...")

 # Define column order
 id_cols = ['Region', 'District', 'Class', 'Latitude', 'Longitude']

 hiv_cols = ['HIV_Prev_Total_pct', 'HIV_Prev_Women_pct', 'HIV_Prev_Men_pct']

 behavioural_cols = [
 'Condom_Use_Women_pct', 'Condom_Use_Men_pct',
 'HighRisk_Sex_Women_pct', 'HighRisk_Sex_Men_pct',
 'HIV_Awareness_Women_pct', 'HIV_Awareness_Men_pct',
 'PMTCT_Knowledge_Women_pct', 'PMTCT_Knowledge_Men_pct',
 'VCT_Women_pct', 'VCT_Men_pct', 'VCT_12mo_Women_pct',
 'Refuse_Sex_Women_pct', 'Ask_Condom_STI_Women_pct',
 'Modern_Contraception_pct', 'Unmet_FP_Need_pct',
 'Adolescent_Fertility_Rate', 'Wife_Beating_Accept_pct'
 ]

 socioeconomic_cols = [
 'Poverty_Incidence_pct', 'Poverty_Intensity_pct',
 'Illiteracy_Rate_pct', 'Uninsured_Rate_pct', 'Unemployment_Rate_pct',
 'Youth_Dependency_Ratio', 'Total_Pop',
 'Literacy_Women_pct', 'Secondary_Edu_Women_pct', 'Edu_Secondary_Women_pct',
 'No_Education_Women_pct', 'No_Insurance_Women_pct', 'No_Insurance_Men_pct'
 ]

 spatial_analysis_cols = [
 'LISA_Cluster_Type', 'LISA_Local_Morans_I', 'LISA_P_Value', 'LISA_Significant_Flag'
 ]

 source_cols = [
 'Data_Source_HIV_Prevalence', 'Data_Source_Behavioural',
 'Data_Source_Socioeconomic', 'Data_Source_Insurance',
 'Data_Source_Education', 'Data_Source_Spatial_Boundaries'
 ]

 # Combine in order
 ordered_cols = (id_cols + hiv_cols + behavioural_cols +
 socioeconomic_cols + spatial_analysis_cols + source_cols)

 # Keep only columns that exist in df
 existing_cols = [col for col in ordered_cols if col in df.columns]

 df = df[existing_cols]

 print(f" Final column count: {len(existing_cols)}")

 return df

def validate_and_summarize(df):
 """Validate dataset and print summary statistics."""
 print("\n" + "="*70)
 print("VALIDATION & SUMMARY")
 print("="*70)

 print(f"\nDataset Shape: {df.shape[0]} districts × {df.shape[1]} columns")

 print(f"\nColumn List ({len(df.columns)} total):")
 for i, col in enumerate(df.columns, 1):
 print(f" {i:2d}. {col}")

 print(f"\nMissing Data Summary:")
 missing = df.isnull().sum()
 missing = missing[missing > 0].sort_values(ascending=False)
 if len(missing) > 0:
 for col, count in missing.items():
 pct = (count / len(df)) * 100
 print(f" {col}: {count} ({pct:.1f}%)")
 else:
 print(" No missing values detected")

 print(f"\nRegional Distribution:")
 print(df['Region'].value_counts().to_string())

 print(f"\nDistrict Class Distribution:")
 print(df['Class'].value_counts().to_string())

 print(f"\nFirst 3 Rows (ID, HIV, and Key Indicators):")
 cols_to_show = ['Region', 'District', 'Class', 'HIV_Prev_Total_pct', 'HIV_Prev_Women_pct',
 'Poverty_Incidence_pct', 'Illiteracy_Rate_pct', 'LISA_Cluster_Type']
 print(df[cols_to_show].head(3).to_string())

 print(f"\nData Type Summary:")
 dtype_summary = {}
 for col in df.columns:
 dtype = str(df[col].dtype)
 if dtype not in dtype_summary:
 dtype_summary[dtype] = 0
 dtype_summary[dtype] += 1

 for dtype, count in sorted(dtype_summary.items()):
 print(f" {dtype}: {count} columns")

 return df

def main():
 """Build and save the master dataset."""
 print("\n" + "="*70)
 print("GHANA HIV SPATIAL EPIDEMIOLOGY - MASTER DATASET BUILDER")
 print("="*70)

 # Load data
 df_base, df_lisa, df_morans, df_spatial_lag = load_source_data()

 # Filter to 260 core districts
 df_260 = filter_to_260_core(df_base, df_lisa)

 # Merge LISA results
 df_master = merge_lisa_results(df_260, df_lisa)

 # Add data source attribution
 df_master = add_data_source_attribution(df_master)

 # Reorder columns logically
 df_master = reorder_columns(df_master)

 # Validate and summarize
 df_master = validate_and_summarize(df_master)

 # Save master dataset
 output_file = 'Ghana_HIV_Spatial_Analysis_MASTER.csv'
 df_master.to_csv(output_file, index=False)
 print(f"\nSaved: {output_file}")

 print("\n" + "="*70)
 print("BUILD COMPLETE")
 print("="*70)
 print(f"\nOutput file: {output_file}")
 print(f"Records: {df_master.shape[0]}")
 print(f"Columns: {df_master.shape[1]}")
 print(f"\nReady for journal submission with full provenance attribution.")

 return df_master

if __name__ == '__main__':
 df = main()
