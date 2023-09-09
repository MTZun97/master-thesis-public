import pandas as pd
import numpy as np
from lcoh import cash_flow
import matplotlib.pyplot as plt


# SMR & SMR with CCUS
gas_price = [0.23] * 10
lcoh_smr  = [(i * 5.08) + 0.3918 for i in gas_price]
lcoh_smr_ccus = [i*1.3 for i in lcoh_smr]

#Electrolysis
lcoe_value = np.arange(0.01, 0.11, 0.01).round(3)
df = pd.read_csv("excel/cost_reduction.csv", index_col=0)
alk_cost = df.loc[2021, "alk_doublef_sl"]
pem_cost = df.loc[2021, "pem_doublef_sl"]
alk_eff  = df.loc[2021, "eff_singlef_alk"]
pem_eff  = df.loc[2021, "eff_singlef_pem"]
lcoh_alk = []
for i in lcoe_value:
    lcoh, _, _, _ = cash_flow(startup_year= 2020, cap_factor= 0.5, current_density=0.25, stack_percent= 0.5,
                                                         electrolyzer_cost= alk_cost, electrolyzer_efficiency= alk_eff, mech_percent = 0.2,
                                                         elect_percent = 0.3,
                                                         elect_df= (pd.DataFrame({"year": range(1983, 2100),
                                                                                  "electricity_price": [i] * len(range(1983, 2100))})
                                                                    .set_index("year")))
    lcoh_alk.append(lcoh)

lcoh_pem = []
for i in lcoe_value:
    lcoh, _, _, _ = cash_flow(startup_year= 2020, cap_factor= 0.5, current_density=2, stack_percent= 0.6,
                                                         electrolyzer_cost= pem_cost, electrolyzer_efficiency= pem_eff, mech_percent = 0.2,
                                                         elect_percent = 0.2,
                                                         elect_df= (pd.DataFrame({"year": range(1983, 2100), 
                                                                                  "electricity_price": [i] * len(range(1983, 2100))}).set_index("year")))
    lcoh_pem.append(lcoh)

#Carbon Tax (350USD/tCO2 - Paris Agreement)
lcoh_smr_CO2_350 = [i + 3.5 for i in lcoh_smr]
lcoh_smr_ccus_CO2_350 = [i + (3.5*0.1) for i in lcoh_smr]

#Carbon Tax (100USD/tCO2 - Net zero)
lcoh_smr_CO2_100 = [i + 1 for i in lcoh_smr]
lcoh_smr_ccus_CO2_100 = [i + (1*0.1) for i in lcoh_smr]

dict = {"electricity_price": lcoe_value, "alkaline_electrolysis": lcoh_alk, "PEM_electrolysis": lcoh_pem,
        "SMR (20USD/MWh)": lcoh_smr, "SMR-CCUS (20 USD/MWh)": lcoh_smr_ccus, "SMR - Carbon Tax (350 USD/tCO2)": lcoh_smr_CO2_350,
        "SMR - CCUS - Carbon Tax (350 USD/tCO2)": lcoh_smr_ccus_CO2_350, "SMR - Carbon Tax (100 USD/tCO2)": lcoh_smr_CO2_100,
        "SMR - CCUS - Carbon Tax (100 USD/tCO2)": lcoh_smr_ccus_CO2_100,}

lcoh_comp = pd.DataFrame.from_dict(dict).set_index("electricity_price")


import seaborn as sns
import matplotlib.pyplot as plt

# Define the colors and line styles for specific groups
color_dict = {'alkaline_electrolysis': (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
              "PEM_eletrolysis":(0.2980392156862745, 0.4470588235294118, 0.6901960784313725)}
line_style_dict = {'SMR-CCUS (20 USD/MWh)': '--', 'SMR - CCUS - Carbon Tax (350 USD/tCO2)': '--', 'SMR - CCUS - Carbon Tax (100 USD/tCO2)': '--'}


plt.figure(figsize=(16, 7))
for column in lcoh_comp.columns:
    sns.lineplot(data=lcoh_comp, x=lcoh_comp.index, y=column, label=column,
                 color=color_dict.get(column, None),  # Use specific color for defined groups
                 linestyle=line_style_dict.get(column, '-'))  # Use dotted line for CCUS

# Generate positions and labels
positions = np.linspace(lcoh_comp.index.min(), lcoh_comp.index.max(), len(range(10, 101, 10)))
labels = range(10, 101, 10)

plt.xticks(positions, labels, rotation=90, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.title('LCOH Comparison with Grey and Blue Hydrogen', fontsize = 18, fontweight = "bold")
plt.xlabel('Electricity Price (USD/MWh)', fontsize = 16, fontweight = "bold")
plt.ylabel('LCOH [USD/kgH2]', fontsize = 16, fontweight = "bold")
plt.grid(linestyle = "dashed", linewidth = 1, alpha =0.6)
plt.legend()
plt.savefig("figures/lcoh_comp", dpi=300, bbox_inches='tight')

plt.show()
