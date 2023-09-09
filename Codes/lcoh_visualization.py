import pandas as pd
from index import valid_sources, lcoe, lcoe_constant
from lcoh import cash_flow
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("excel/cost_reduction.csv", index_col=0)
cap_factor_sources = {"bioenergy_lcoe": 0.53, "offshore_wind_lcoe": 0.23, "solar_lcoe": 0.12, "hydro_lcoe": 0.45, "onshore_wind_lcoe": 0.23}
settings = {
    'low': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef_sl", 'eff': "eff_singlef_alk"}, 
            'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef_sl", 'eff': "eff_singlef_pem"}},
    'high': {'alk': {'params': {"current_density": 0.5, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef", 'eff': "eff_singlef_alk"}, 
             'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef", 'eff': "eff_singlef_pem"}}
}

lcoh_data = {}

def calculate_data(setting_type):
    for tech_type in ['alk', 'pem']:
        data = []
        setting = settings[setting_type][tech_type]
        for index in df.index:
            electrolyzer_cost = df.loc[index, setting['cost']]
            electrolyzer_efficiency = df.loc[index, setting['eff']]
            lcoh_row = {"Index": index}
            for source in valid_sources:
                cap_factor = cap_factor_sources.get(source, 0.8)
                lcoh, _, _, _ = cash_flow(startup_year=index, cap_factor=cap_factor, electrolyzer_cost=electrolyzer_cost, electrolyzer_efficiency=electrolyzer_efficiency, elect_df=lcoe(source, "World") if setting_type=='low' else lcoe_constant(source, "World"), **setting['params'])
                lcoh_row[source] = lcoh
            data.append(lcoh_row)
        lcoh_data[f"{setting_type}_{tech_type}"] = pd.DataFrame(data).set_index('Index')

calculate_data('low')
calculate_data('high')

lcoh_data['average_alk'] = (lcoh_data['low_alk'] + lcoh_data['high_alk']) / 2
lcoh_data['average_pem'] = (lcoh_data['low_pem'] + lcoh_data['high_pem']) / 2

with pd.ExcelWriter('excel/lcoh_data.xlsx') as writer:
    for key in lcoh_data:
        lcoh_data[key].to_excel(writer, sheet_name=key)


sources = ['offshore_wind_lcoe', 'solar_lcoe', 'onshore_wind_lcoe']
colors = sns.color_palette("deep", len(sources))
sns.set_style("whitegrid")
plt.figure(figsize=(16, 5))
for idx, source in enumerate(sources):
    # Alkaline plots
    plt.fill_between(lcoh_data['low_alk'].index, lcoh_data['low_alk'][source], lcoh_data['high_alk'][source], color=colors[idx], alpha=0.3)
    plt.plot(lcoh_data['average_alk'].index, lcoh_data['average_alk'][source], color=colors[idx], label=f'{source}')

plt.title("Global Levelized Cost of Hydrogen for Alkaline Electrolyzers", fontsize=18, fontweight='bold')
plt.xlabel("Year", fontsize=16, fontweight='bold')
plt.xticks(range(1990, 2051, 1), range(1990, 2051, 1), rotation=90, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.grid(linestyle="dashed", linewidth=1, alpha = 0.6)
plt.ylabel("Levelized Cost of Hydrogen", fontsize=16, fontweight='bold')
plt.legend(loc='best')
plt.savefig("figures/global_alkaline_lcoh.png", dpi=300, bbox_inches="tight")

# Clearing labels for the second plot
plt.figure(figsize=(16, 5))
for idx, source in enumerate(sources):
    # PEM plots
    
    plt.fill_between(lcoh_data['low_pem'].index, lcoh_data['low_pem'][source], lcoh_data['high_pem'][source], color=colors[idx], alpha=0.3)
    plt.plot(lcoh_data['average_pem'].index, lcoh_data['average_pem'][source], color=colors[idx], label=f'{source}')

plt.title("Global Levelized Cost of Hydrogen for PEM Electrolyzers", fontsize=18, fontweight='bold')
plt.xlabel("Year", fontsize=16, fontweight='bold')
plt.xticks(range(1990, 2051, 1), range(1990, 2051, 1), rotation=90, fontsize=16, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.grid(linestyle="dashed", linewidth=1, alpha = 0.6)
plt.ylabel("Levelized Cost of Hydrogen", fontsize=16, fontweight='bold')
plt.legend(loc='best')
plt.savefig("figures/global_pem_lcoh.png", dpi=300, bbox_inches="tight")

