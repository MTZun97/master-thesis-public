import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from lcoh import cash_flow

# Define the base parameters
params = {
    "startup_year": 2020,
    "cap_factor": 0.5,
    "current_density": 2,
    "stack_percent": 0.6,
    "electrolyzer_cost": 1000,
    "electrolyzer_efficiency": 50,
    "mech_percent": 0.2,
    "elect_percent": 0.2,
    "water_rate": 0.00237495008,
    "elect_df": (pd.DataFrame.from_dict({"year": range(1983, 2100), "electricity_price": [0.036] * len(range(1983, 2100))})
                 .set_index("year"))
}

# Create params_low by updating parameter values
params_low = {
    "startup_year": params["startup_year"],
    "cap_factor": params["cap_factor"] * 1.3,
    "current_density": params["current_density"],
    "stack_percent": params["stack_percent"],
    "electrolyzer_cost": params["electrolyzer_cost"] * 0.7,
    "electrolyzer_efficiency": params["electrolyzer_efficiency"] * 1.3,
    "mech_percent": params["mech_percent"],
    "elect_percent": params["elect_percent"],
    "water_rate": params["water_rate"] * 0.7,
    "elect_df": params["elect_df"].copy()
}
params_low["elect_df"]["electricity_price"] *= 0.7
# Create params_high by updating parameter values
params_high = {
    "startup_year": params["startup_year"],
    "cap_factor": params["cap_factor"] * 0.7,
    "current_density": params["current_density"],
    "stack_percent": params["stack_percent"],
    "electrolyzer_cost": params["electrolyzer_cost"] * 1.3,
    "electrolyzer_efficiency": params["electrolyzer_efficiency"] * 0.7,
    "mech_percent": params["mech_percent"],
    "elect_percent": params["elect_percent"],
    "water_rate": params["water_rate"] * 1.3,
    "elect_df": params["elect_df"].copy()
}
params_high["elect_df"]["electricity_price"] *= 1.3

lcoh_low = {}
lcoh_base = {}
lcoh_high = {}

lcoh_base["cap_factor"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_low["cap_factor"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params_low["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_high["cap_factor"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params_high["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])

lcoh_base["electrolyzer_cost"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_low["electrolyzer_cost"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params_low["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_high["electrolyzer_cost"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params_high["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])

lcoh_base["electrolyzer_efficiency"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_low["electrolyzer_efficiency"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params_low["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_high["electrolyzer_efficiency"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params_high["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])


lcoh_base["electricity"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"])
lcoh_low["electricity"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params_low["elect_df"])
lcoh_high["electricity"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params_high["elect_df"])

lcoh_base["water"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"], 
                                    water_rate= params["water_rate"])
lcoh_low["water"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"], 
                                    water_rate= params_low["water_rate"])
lcoh_high["water"], _,_,_ = cash_flow(startup_year= 2020, cap_factor= params["cap_factor"], current_density=params["current_density"], 
                                     stack_percent= params["stack_percent"], electrolyzer_cost= params["electrolyzer_cost"], 
                                     electrolyzer_efficiency= params["electrolyzer_efficiency"], mech_percent = params["mech_percent"],
                                    elect_percent = params["elect_percent"], elect_df= params["elect_df"], 
                                    water_rate= params_high["water_rate"])

#Calculate the percentage change
keys = lcoh_base.keys()
percentage_change = {key: {"low": (lcoh_low[key] - lcoh_base[key]) / lcoh_base[key] * 100,
                           "high": (lcoh_high[key] - lcoh_base[key]) / lcoh_base[key] * 100} for key in keys}



# Order keys by the absolute maximum percentage change
ordered_keys = sorted(keys, key=lambda x: max(abs(percentage_change[x]["low"]), abs(percentage_change[x]["high"])), reverse=False)

# Prepare data for the tornado chart
low_data = [percentage_change[key]["low"] for key in ordered_keys]
high_data = [percentage_change[key]["high"] for key in ordered_keys]

# Create a tornado chart
fig, ax = plt.subplots(figsize = (7,5))

bar_width = 0.4
y_vals = range(len(ordered_keys))
ax.barh(y_vals, low_data, color=(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), edgecolor='gray', height=bar_width)
ax.barh(y_vals, high_data, color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725), edgecolor='gray', height=bar_width)

new_labels = ['water\n-30%,+30%', 'electrolyzer_cost\n-30%,+30%', 'capacity_factor\n+30%,-30%', 
              'LCOE\n-30%,+30%', 'efficiency\n+30%,-30%'] 

ax.set_yticks(y_vals)
ax.set_yticklabels(new_labels, ha = "center", fontsize=10, fontweight='bold', font = "Arial")
ax.set_xticklabels(fontsize=10, fontweight='bold', font = "Arial")
ax.yaxis.set_tick_params(pad=45)
plt.xlabel("Percentage Change in LCOH (%)", fontsize = 16, fontweight = "bold", font = "Arial")
plt.ylabel("Parmeters", fontsize = 16, fontweight = "bold", font = "Arial")
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("figures/lcoh_sensitivity_pem.png", dpi=300, bbox_inches='tight')

