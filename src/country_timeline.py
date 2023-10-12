import pandas as pd
import plotly.graph_objects as go
import os
from plotly.subplots import make_subplots

# Step 1: Load data
countries = ["Canada", "Denmark", "Sweden", "China", "France", "Germany", "Japan", "United States", "United Kingdom", "Spain", "Australia", "Netherlands"]
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "lcoh_data.xlsx"))

df_low = {}
df_high = {}
with pd.ExcelFile(file_path) as reader:
    for country in countries:
        df_low[country] = pd.read_excel(reader, sheet_name=f'df_low_{country}', index_col='Index')
        df_high[country] = pd.read_excel(reader, sheet_name=f'df_high_{country}', index_col='Index')

def get_earliest_year(df_data, target):
    results_dfs = []
    for country, df_country in df_data.items():
        earliest_years = {source: df_country[source].loc[df_country[source] < target].index[0] if df_country[source].loc[df_country[source] < target].index.any() else None for source in df_country.columns}
        earliest_years['Country'] = country
        results_dfs.append(pd.DataFrame([earliest_years]))
    results_df = pd.concat(results_dfs, ignore_index=True)
    return results_df


def create_trace(df_low, df_high, color_low, color_high, sources_symbols, countries):
    traces = []
    for source, symbol in sources_symbols.items():
        for country in countries:
            country_data_low = df_low[(df_low['Country'] == country) & (df_low['Source'] == source)]
            country_data_high = df_high[(df_high['Country'] == country) & (df_high['Source'] == source)]
            
            if not country_data_low.empty:
                traces.append(
                    go.Scatter(
                        x=country_data_low['Year'].values,
                        y=[country for _ in range(len(country_data_low['Year'].values))],
                        mode='markers',
                        name=f"Optimistic - {source}",
                        marker=dict(color=color_low, size=15, symbol=symbol),
                        legendgroup=source,
                        showlegend=False
                    )
                )
            if not country_data_high.empty:
                traces.append(
                    go.Scatter(
                        x=country_data_high['Year'].values,
                        y=[country for _ in range(len(country_data_high['Year'].values))],
                        mode='markers',
                        name=f"Pessimistic - {source}",
                        marker=dict(color=color_high, size=15, symbol=symbol),
                        legendgroup=source,
                        showlegend=False
                    )
                )
            
            if (country in ["Canada", "Sweden", "Denmark"] and source == "solar_lcoe") or (country in ["Australia", "Netherlands"] and source == "onshore_wind_lcoe"):
                traces.append(
                    go.Scatter(
                        x=[2047],  # Adjust the x-coordinate as necessary
                        y=[country],
                        mode='text',
                        name=f"No Data - {source}",
                        text="No Data",
                        textfont=dict(size=16, color='gray'),  # Set your desired font size and color
                        legendgroup=source,
                        showlegend=False,
                        hoverinfo='y+text'
                    )
                )
    return traces

def create_timeline_plot(cost_target):
    results_df_low = get_earliest_year(df_low, cost_target)
    results_df_low = results_df_low.melt(id_vars=['Country'], var_name='Source', value_name='Year')

    results_df_high = get_earliest_year(df_high, cost_target)
    results_df_high = results_df_high.melt(id_vars=['Country'], var_name='Source', value_name='Year')

    min_year = min(results_df_low['Year'].min(), results_df_high['Year'].min())-5
    max_year = 2050

    colors = {'Optimistic': '#636EFA', 'Pessimistic': '#FF6692'}
    sources_symbols = {'solar_lcoe': 'circle', 'onshore_wind_lcoe': 'square'}
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Solar Energy", "Onshore Wind Energy"), shared_yaxes=True, horizontal_spacing=0.05, vertical_spacing=0.1)
    for trace in create_trace(results_df_low, results_df_high, colors['Optimistic'], colors['Pessimistic'], sources_symbols, countries):
        col = 1 if 'solar' in trace.name else 2
        fig.add_trace(trace, row=1, col=col)

    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 16  # or whatever font size you want


    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color=colors['Optimistic'], width=2),
            name='Optimistic',
            showlegend=True
        ),
        row=1, col=1  # Add to the first subplot (solar graph)
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='lines',
            line=dict(color=colors['Pessimistic'], width=2),
            name='Pessimistic',
            showlegend=True
        ),
        row=1, col=1  # Add to the first subplot (solar graph)
    )

    # Update layout
    fig.update_layout(
        yaxis=dict(
            tickfont=dict(family='Arial, bold', size=16),
        ),
        xaxis=dict(
            tickfont=dict(family='Arial, bold', size=16),
        ),
        xaxis2=dict(
            tickfont=dict(family='Arial, bold', size=16),  # Adjust the font size here for the second subplot
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(
                family="Arial Bold",
                size=16,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
            itemsizing='constant'
        ),
        legend_title_text=''
    )
    fig.update_xaxes(range=[min_year, max_year])

    return fig
