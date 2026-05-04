#!/usr/bin/env python3
"""
HIV Spatial Epidemiology Dashboard — Ghana 260 Districts
Interactive Dash application with spatial analysis and ML feature importance
"""

import os
import json
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DATA LOADING
# ============================================================================

# Get absolute path for data files
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_data():
 """Load all required datasets"""
 # Main dataset
 df = pd.read_csv(os.path.join(script_dir, 'Ghana_HIV_Analysis_Dataset_260districts.csv'))
 
 # LISA results
 lisa = pd.read_csv(os.path.join(script_dir, 'LISA_Results.csv'))
 
 # Spatial lag results
 slag = pd.read_csv(os.path.join(script_dir, 'Spatial_Lag_Regression_Results.csv'))
 
 # ML results
 with open(os.path.join(script_dir, 'ml_analysis_results.json'), 'r') as f:
 ml = json.load(f)
 
 # Moran's I results
 moran = pd.read_csv(os.path.join(script_dir, 'Morans_I_Results.csv'))
 
 # GeoJSON
 with open('/sessions/blissful-exciting-keller/mnt/uploads/Ghana_New_260_District.geojson', 'r') as f:
 geojson = json.load(f)
 
 return df, lisa, slag, ml, moran, geojson

# Load data once
df, lisa, slag, ml, moran, geojson = load_data()

# ============================================================================
# DATA PREPARATION
# ============================================================================

# Prepare regional aggregates for choropleth
regional_hiv = df.groupby('Region').agg({
 'HIV_Prev_Total_pct': 'mean',
 'Total_Pop': 'sum',
 'VCT_Women_pct': 'mean',
 'VCT_Men_pct': 'mean'
}).reset_index()
regional_hiv['VCT_uptake'] = (regional_hiv['VCT_Women_pct'] + regional_hiv['VCT_Men_pct']) / 2

# Prepare correlation matrix
key_vars = ['HIV_Prev_Total_pct', 'VCT_Women_pct', 'Condom_Use_Women_pct',
 'Poverty_Incidence_pct', 'Illiteracy_Rate_pct', 'Modern_Contraception_pct',
 'HIV_Awareness_Women_pct', 'Unmet_FP_Need_pct']
corr_matrix = df[key_vars].corr()

# Prepare LASSO features (top 5)
lasso_features = ml['LASSO_Results']['Top_5_Features']
lasso_df = pd.DataFrame(lasso_features)
lasso_df['Coefficient'] = lasso_df['Coefficient'].abs()
lasso_df = lasso_df.sort_values('Coefficient', ascending=True)

# Regional scatter data
scatter_data = df.groupby('Region').agg({
 'HIV_Prev_Total_pct': 'mean',
 'VCT_Women_pct': 'mean',
 'Total_Pop': 'sum'
}).reset_index()

# ============================================================================
# APP INITIALIZATION
# ============================================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "HIV Spatial Epidemiology Dashboard — Ghana"

# Color scheme
color_primary = '#2E86AB'
color_secondary = '#A23B72'
color_success = '#18A558'

# ============================================================================
# FIGURE CREATION FUNCTIONS
# ============================================================================

def create_choropleth_map():
 """Create regional HIV prevalence choropleth"""
 fig = go.Figure(data=go.Choropleth(
 z=regional_hiv['HIV_Prev_Total_pct'],
 locations=regional_hiv['Region'],
 locationmode='geojson-id',
 colorscale='YlOrRd',
 marker_line_width=0.5,
 colorbar=dict(
 title="HIV Prev. (%)",
 thickness=15,
 len=0.7
 ),
 text=regional_hiv['Region'],
 hovertemplate='<b>%{text}</b><br>HIV Prevalence: %{z:.2f}%<extra></extra>'
 ))
 
 fig.update_layout(
 title='HIV Prevalence by Region (%)',
 geo=dict(
 scope='africa',
 projection_type='natural earth',
 showland=True,
 landcolor='rgb(243, 243, 243)',
 coastcolor='rgb(200, 200, 200)'
 ),
 height=500,
 margin=dict(l=0, r=0, t=40, b=0)
 )
 return fig

def create_correlation_heatmap():
 """Create correlation matrix heatmap"""
 fig = go.Figure(data=go.Heatmap(
 z=corr_matrix.values,
 x=corr_matrix.columns,
 y=corr_matrix.columns,
 colorscale='RdBu',
 zmid=0,
 zmin=-1,
 zmax=1,
 text=np.round(corr_matrix.values, 2),
 texttemplate='%{text:.2f}',
 textfont={"size": 9},
 colorbar=dict(title="Correlation")
 ))
 
 fig.update_layout(
 title='Correlation Matrix: Key Variables',
 height=600,
 xaxis_tickangle=-45,
 margin=dict(b=150, l=100, r=50, t=50)
 )
 return fig

def create_lasso_features_chart():
 """Create LASSO feature importance chart"""
 fig = go.Figure(go.Bar(
 y=lasso_df['Feature'],
 x=lasso_df['Coefficient'],
 orientation='h',
 marker=dict(
 color=lasso_df['Coefficient'],
 colorscale='Viridis',
 showscale=False
 ),
 text=np.round(lasso_df['Coefficient'].values, 3),
 textposition='outside'
 ))
 
 fig.update_layout(
 title='Top 5 LASSO Coefficients (Absolute)',
 xaxis_title='Absolute Coefficient Value',
 yaxis_title='Feature',
 height=400,
 margin=dict(l=250, r=80, t=50, b=50)
 )
 return fig

def create_spatial_lag_table():
 """Create spatial lag regression table"""
 return slag.copy()

def create_scatter_plot(selected_region=None):
 """Create HIV prevalence vs VCT uptake scatter plot"""
 data = scatter_data.copy()
 data['size'] = np.log10(data['Total_Pop']) + 1
 
 colors = ['#18A558' if r == selected_region else '#2E86AB' for r in data['Region']]
 
 fig = go.Figure()
 
 for region in data['Region']:
 row = data[data['Region'] == region].iloc[0]
 color = '#18A558' if region == selected_region else '#2E86AB'
 size = row['size']
 
 fig.add_trace(go.Scatter(
 x=[row['VCT_Women_pct']],
 y=[row['HIV_Prev_Total_pct']],
 mode='markers',
 marker=dict(
 size=size * 5,
 color=color,
 opacity=0.7,
 line=dict(width=1, color='white')
 ),
 text=region,
 hovertemplate='<b>%{text}</b><br>VCT Uptake: %{x:.1f}%<br>HIV Prev: %{y:.2f}%<extra></extra>',
 name=region,
 showlegend=False
 ))
 
 fig.update_layout(
 title='HIV Prevalence vs VCT Uptake by Region (bubble size = population)',
 xaxis_title='VCT Uptake (%)',
 yaxis_title='HIV Prevalence (%)',
 height=500,
 hovermode='closest',
 margin=dict(l=60, r=50, t=50, b=60)
 )
 
 return fig

# ============================================================================
# APP LAYOUT
# ============================================================================

app.layout = dbc.Container([
 dbc.Row([
 dbc.Col([
 html.H1("HIV Spatial Epidemiology Dashboard — Ghana 260 Districts",
 className="text-center mb-4 mt-4",
 style={'color': color_primary, 'fontWeight': 'bold'})
 ])
 ]),
 
 # KPI Cards
 dbc.Row([
 dbc.Col([
 dbc.Card([
 dbc.CardBody([
 html.H5("Mean HIV Prevalence (%)", className="card-title"),
 html.H3(f"{df['HIV_Prev_Total_pct'].mean():.2f}%", 
 style={'color': color_primary})
 ])
 ], className="mb-3")
 ], width=12, lg=3),
 
 dbc.Col([
 dbc.Card([
 dbc.CardBody([
 html.H5("Moran's I (HIV Prev.)", className="card-title"),
 html.H3(f"{moran[moran['Variable']=='HIV_Prev_Total_pct']['Morans_I'].values[0]:.3f}",
 style={'color': color_secondary})
 ])
 ], className="mb-3")
 ], width=12, lg=3),
 
 dbc.Col([
 dbc.Card([
 dbc.CardBody([
 html.H5("Spatial Lag ρ", className="card-title"),
 html.H3(f"{slag[slag['Variable']=='W_HIV_Prev_Total_pct']['Coefficient'].values[0]:.3f}",
 style={'color': color_success})
 ])
 ], className="mb-3")
 ], width=12, lg=3),
 
 dbc.Col([
 dbc.Card([
 dbc.CardBody([
 html.H5("LASSO R²", className="card-title"),
 html.H3(f"{ml['Model_Comparison']['LASSO_vs_RF']['LASSO_R2']:.4f}",
 style={'color': '#F18F01'})
 ])
 ], className="mb-3")
 ], width=12, lg=3),
 ], className="mb-4"),
 
 # Charts row 1
 dbc.Row([
 dbc.Col([
 dcc.Graph(id='choropleth-map', figure=create_choropleth_map())
 ], width=12, lg=6),
 
 dbc.Col([
 dcc.Graph(id='lasso-features', figure=create_lasso_features_chart())
 ], width=12, lg=6),
 ], className="mb-4"),
 
 # Charts row 2
 dbc.Row([
 dbc.Col([
 dcc.Graph(id='correlation-heatmap', figure=create_correlation_heatmap())
 ], width=12, lg=6),
 
 dbc.Col([
 html.H5("Spatial Lag Regression Coefficients", className="mt-3 mb-3",
 style={'color': color_primary}),
 html.Div(id='spatial-lag-table', children=[
 dbc.Table.from_dataframe(
 create_spatial_lag_table().round(6),
 striped=True,
 bordered=True,
 hover=True,
 responsive=True,
 size='sm'
 )
 ], style={'maxHeight': '500px', 'overflowY': 'auto'})
 ], width=12, lg=6),
 ], className="mb-4"),
 
 # Scatter plot with selector
 dbc.Row([
 dbc.Col([
 html.Label("Select Region to Highlight:", style={'fontWeight': 'bold'}),
 dcc.Dropdown(
 id='region-selector',
 options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())],
 value=None,
 placeholder="Choose a region...",
 style={'width': '100%'}
 )
 ], width=12, lg=4),
 ], className="mb-3"),
 
 dbc.Row([
 dbc.Col([
 dcc.Graph(id='scatter-plot')
 ], width=12)
 ], className="mb-5"),
 
], fluid=True, style={'backgroundColor': '#f8f9fa', 'paddingBottom': '50px'})

# ============================================================================
# CALLBACKS
# ============================================================================

@callback(
 Output('scatter-plot', 'figure'),
 Input('region-selector', 'value')
)
def update_scatter(selected_region):
 return create_scatter_plot(selected_region)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
 print("Starting HIV Spatial Epidemiology Dashboard...")
 print("Open http://127.0.0.1:8050 in your browser")
 app.run_server(debug=True, host='127.0.0.1', port=8050)
