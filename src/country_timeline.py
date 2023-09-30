import pandas as pd
from lcoh import valid_sources, lcoe, lcoe_constant
from lcoh import cash_flow
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
import dash
import os

countries = ["Australia", "Germany", "China", "Japan", "Canada", "United States", "United Kingdom", "Sweden", "Spain", "France", "Denmark"]
csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "lcoh_data.xlsx"))
df_low = {}
df_high = {}
with pd.ExcelFile(csv_file_path) as reader:
    for country in countries:
        df_low[country] = pd.read_excel(reader, sheet_name=f'df_low_{country}', index_col='Index')
        df_high[country] = pd.read_excel(reader, sheet_name=f'df_high_{country}', index_col='Index')

def get_earliest_year(df_data, target):
    results_dfs = []  # This will store individual dataframes which will be concatenated later

    for country, df_country in df_data.items():
        earliest_years = [(source, df_country[source].loc[df_country[source] < target].index[0]) for source in df_country.columns if df_country[source].loc[df_country[source] < target].index.any()]
        earliest_years.sort(key=lambda x: x[1])
        
        # Creating a DataFrame for each iteration and storing it in the list
        results_dfs.append(pd.DataFrame([{'Country': country, 'Source': earliest_years[0][0] if earliest_years else None, 'Year': earliest_years[0][1] if earliest_years else None}]))

    results_df = pd.concat(results_dfs, ignore_index=True)  # Concatenating all the dataframes in the list
    return results_df



def create_timeline_plot(cost_target):
    # Convert tuple colors to hexadecimal

    results_df_low = get_earliest_year(df_low, target = cost_target)
    results_df_high = get_earliest_year(df_high, target= cost_target)
    # Convert tuple colors to hexadecimal
    colors = ['#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)) 
            for r, g, b in [(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), 
                            (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)]]

    fig = go.Figure()

    sources_symbols = {'solar_lcoe': 'circle', 'onshore_wind_lcoe': 'square'}

    # Add a trace for each country in the low and high data
    for df, trace_name, color in zip([results_df_low, results_df_high], ['Optimistic', 'Pessimistic'], colors):
        for idx, row in df.iterrows():
            if pd.isna(row['Year']):
                continue

            fig.add_trace(go.Scatter(
                x=[row['Year'], 2052],
                y=[row['Country'], row['Country']],
                mode='lines+markers',
                name=trace_name,
                line=dict(color=color, width=10),
                marker=dict(color=color, size=20, symbol=sources_symbols.get(row['Source'])),
                legendgroup=trace_name,
                hovertemplate='<i>%{y}</i><br>Year: %{x}',
                showlegend=False  # Do not show the legend for these traces
            ))

    # Add dummy traces for legend
    for trace_name, color in zip(['Optimistic', 'Pessimistic'], colors):
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            name=trace_name,
            line=dict(color=color, width=2),
            showlegend=True
        ))

    # Add dummy traces for source types
# Add dummy traces for source types
    for source, symbol in sources_symbols.items():
        fig.add_trace(go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            name=source,
            marker=dict(
                symbol=symbol, 
                size=10, 
                line=dict(color='rgba(0,0,0,1)', width=2), # This sets the marker edge color to black
                color='rgba(255, 255, 255, 0)' # This sets the marker fill color to transparent
            ),
            showlegend=True
        ))


    # Update layout
    fig.update_layout(
        title='<b>Timeline Plot of Countries to Achieve target LCOH<b>',
        title_font=dict(size=18, family='Arial', color='black'),title_x = 0.5,
        xaxis=dict(title='Year', range=[2010, 2050], tickfont=dict(size = 12)),
        yaxis=dict(title='Country', tickfont=dict(size = 12)),
        autosize=True,
        height=500,
    )
    
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
            itemsizing='constant'
        ),
        legend_title_text=''
    )

    return fig

