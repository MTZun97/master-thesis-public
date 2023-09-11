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

df = pd.read_csv("data/cost_reduction.csv", index_col=0)
cap_factor_sources = {"bioenergy_lcoe": 0.3, "offshore_wind_lcoe": 0.5, "solar_lcoe": 0.7, "hydro_lcoe": 0.3, "onshore_wind_lcoe": 0.5}

settings = {
    'low': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef_sl", 'eff': "eff_singlef_alk"}, 
            'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef_sl", 'eff': "eff_singlef_alk"}},
    'high': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef", 'eff': "eff_singlef_alk"}, 
             'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef", 'eff': "eff_singlef_alk"}}
}

countries = ["Australia", "Germany", "China", "Netherlands", "Japan", "Canada", "United States", "United Kingdom", "Sweden", "Spain", "France", "Denmark"]

def calculate_data(setting, lcoe_function):
    df_result = {}
    for country in countries:
        data = []
        for index in df.index:
            electrolyzer_cost = df.loc[index, setting['cost']]
            electrolyzer_efficiency = df.loc[index, setting['eff']]
            lcoh_row = {"Index": index}
            for source in valid_sources:
                cap_factor = cap_factor_sources.get(source, 0.8)
                lcoe_df = pd.DataFrame({"year":range(1983,2100), "electricity_price": list(lcoe_function(source,country).loc[index].values) * len(range(1983,2100))}).set_index("year")
                if lcoe_df is not None:
                    lcoh, _, _, _ = cash_flow(startup_year=index, cap_factor=cap_factor, electrolyzer_cost=electrolyzer_cost, electrolyzer_efficiency=electrolyzer_efficiency, elect_df=lcoe_df, **setting['params'])
                    lcoh_row[source] = lcoh
            data.append(lcoh_row)
        df_result[country] = pd.DataFrame(data).set_index("Index")
    return df_result

def get_earliest_year(df_data, target):
    results_df = pd.DataFrame(columns=['Country', 'Source', 'Year'])
    for country, df_country in df_data.items():
        earliest_years = [(source, df_country[source].loc[df_country[source] < target].index[0]) for source in df_country.columns if df_country[source].loc[df_country[source] < 2].index.any()]
        earliest_years.sort(key=lambda x: x[1])
        results_df = results_df.append({'Country': country, 'Source': earliest_years[0][0] if earliest_years else None, 'Year': earliest_years[0][1] if earliest_years else None}, ignore_index=True)
    return results_df

df_low = calculate_data(settings["low"]["pem"], lcoe)
df_high = calculate_data(settings["high"]["pem"], lcoe_constant)

# After your existing code, add these lines to save df_low and df_high as .xlsx files
with pd.ExcelWriter('data/lcoh_data.xlsx') as writer:
    for country, data in df_low.items():
        data.to_excel(writer, sheet_name=f'df_low_{country}')

    for country, data in df_high.items():
        data.to_excel(writer, sheet_name=f'df_high_{country}')

# To read the data back into df_low and df_high, you can use this code:
df_low = {}
df_high = {}
with pd.ExcelFile('data/lcoh_data.xlsx') as reader:
    for country in countries:
        df_low[country] = pd.read_excel(reader, sheet_name=f'df_low_{country}', index_col='Index')
        df_high[country] = pd.read_excel(reader, sheet_name=f'df_high_{country}', index_col='Index')


