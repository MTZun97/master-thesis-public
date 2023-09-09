import pandas as pd
from index import valid_sources, lcoe, lcoe_constant
from lcoh import cash_flow
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("excel/cost_reduction.csv", index_col=0)
cap_factor_sources = {"bioenergy_lcoe": 0.3, "offshore_wind_lcoe": 0.5, "solar_lcoe": 0.7, "hydro_lcoe": 0.3, "onshore_wind_lcoe": 0.5}

settings = {
    'low': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef_sl", 'eff': "eff_singlef_alk"}, 
            'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef_sl", 'eff': "eff_singlef_alk"}},
    'high': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef", 'eff': "eff_singlef_alk"}, 
             'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef", 'eff': "eff_singlef_alk"}}
}

countries = ["Australia", "Germany", "China", "Netherlands", "Japan", "Canada", "United States", "United Kingdom",
             "Sweden", "Spain", "France", "Denmark", "India", "Italy"]

df_low = {}
for country in countries:
    data = []
    setting = settings["low"]["pem"]
    for index in df.index:
        electrolyzer_cost = df.loc[index, setting['cost']]
        electrolyzer_efficiency = df.loc[index, setting['eff']]
        lcoh_row = {"Index": index}
        for source in valid_sources:
            cap_factor = cap_factor_sources.get(source, 0.8)
            lcoe_df = (pd.DataFrame.from_dict({"year":range(1983,2100), 
                                     "electricity_price": list(lcoe(source,country).loc[index].values) * len(range(1983,2100))})
                       .set_index("year"))
            if lcoe_df is not None:  # Skip calculation if lcoe_df is None
                lcoh, _, _, _ = cash_flow(startup_year=index, cap_factor=cap_factor, 
                                          electrolyzer_cost=electrolyzer_cost, electrolyzer_efficiency=electrolyzer_efficiency, 
                                          elect_df=lcoe_df, **setting['params'])
                lcoh_row[source] = lcoh
        data.append(lcoh_row)
    df_low[country] = pd.DataFrame(data).set_index("Index")


results_df_low = pd.DataFrame(columns=['Country', 'Source', 'Year'])

for country, df_country in df_low.items():
    earliest_years = []
    for source in df_country.columns:
        try:
            earliest_year = df_country[source].loc[df_country[source] < 2].index[0]
            earliest_years.append((source, earliest_year))
        except IndexError:
            # This source never went below 2
            pass
    earliest_years.sort(key=lambda x: x[1])
    if earliest_years:
        # Append the earliest source and year for this country to the results DataFrame
        results_df_low = results_df_low.append({'Country': country, 'Source': earliest_years[0][0], 'Year': earliest_years[0][1]}, ignore_index=True)
    else:
        # Append NaN values if no sources went below 2 for this country
        results_df_low = results_df_low.append({'Country': country, 'Source': np.nan, 'Year': np.nan}, ignore_index=True)


df_high = {}
for country in countries:
    data = []
    setting = settings["high"]["pem"]
    for index in df.index:
        electrolyzer_cost = df.loc[index, setting['cost']]
        electrolyzer_efficiency = df.loc[index, setting['eff']]
        lcoh_row = {"Index": index}
        for source in valid_sources:
            cap_factor = cap_factor_sources.get(source, 0.8)
            lcoe_df = (pd.DataFrame.from_dict({"year":range(1983,2100), 
                                     "electricity_price": list(lcoe_constant(source,country).loc[index].values) * len(range(1983,2100))})
                       .set_index("year"))
            if lcoe_df is not None:  # Skip calculation if lcoe_df is None
                lcoh, _, _, _ = cash_flow(startup_year=index, cap_factor=cap_factor, 
                                          electrolyzer_cost=electrolyzer_cost, electrolyzer_efficiency=electrolyzer_efficiency, 
                                          elect_df=lcoe_df, **setting['params'])
                lcoh_row[source] = lcoh
        data.append(lcoh_row)
    df_high[country] = pd.DataFrame(data).set_index("Index")


results_df_high = pd.DataFrame(columns=['Country', 'Source', 'Year'])

for country, df_country in df_high.items():
    earliest_years = []
    for source in df_country.columns:
        try:
            earliest_year = df_country[source].loc[df_country[source] < 2].index[0]
            earliest_years.append((source, earliest_year))
        except IndexError:
            # This source never went below 2
            pass
    earliest_years.sort(key=lambda x: x[1])
    if earliest_years:
        # Append the earliest source and year for this country to the results DataFrame
        results_df_high = results_df_high.append({'Country': country, 'Source': earliest_years[0][0], 'Year': earliest_years[0][1]}, ignore_index=True)
    else:
        # Append NaN values if no sources went below 2 for this country
        results_df_high = results_df_high.append({'Country': country, 'Source': np.nan, 'Year': np.nan}, ignore_index=True)

print(results_df_high)

import matplotlib.colors as mcolors
import plotly.graph_objects as go

# Convert tuple colors to hexadecimal
colors = ['#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)) 
          for r, g, b in [(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), 
                          (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)]]

fig = go.Figure()

sources_symbols = {'solar_lcoe': 'circle', 'onshore_wind_lcoe': 'square'}

# Add a trace for each country in the low and high data
for df, trace_name, color in zip([results_df_low, results_df_high], ['Low', 'High'], colors):
    for idx, row in df.iterrows():
        if pd.isna(row['Year']):
            continue

        fig.add_trace(go.Scatter(
            x=[row['Year'], 2052],
            y=[row['Country'], row['Country']],
            mode='lines+markers',
            name=trace_name,
            line=dict(color=color, width=10),
            marker=dict(color=color, size=20, symbol=sources_symbols.get(row['Source'], 'circle')),
            legendgroup=trace_name,
            hovertemplate='<i>%{y}</i><br>Year: %{x}<br>Source: %{text}',
            showlegend=False  # Do not show the legend for these traces
        ))

# Add dummy traces for legend
for trace_name, color in zip(['Low', 'High'], colors):
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='lines',
        name=trace_name,
        line=dict(color=color, width=2),
        showlegend=True
    ))

# Add dummy traces for source types
for source, symbol in sources_symbols.items():
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        name=source,
        marker=dict(symbol=symbol, size=10, color=colors[0] if source=='solar_lcoe' else colors[1]),
        showlegend=True
    ))

# Update layout
fig.update_layout(
    title='Timeline Plot of Countries to Achieve LCOH of 2 USD/kg',
    xaxis=dict(title='Year', range=[2000, 2050], tickfont=dict(size = 12)),
    yaxis=dict(title='Country', tickfont=dict(size = 12)),
    autosize=False,
    width=1000,
    height=700,
)

fig.show()
