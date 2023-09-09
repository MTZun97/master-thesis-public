# Importing Libraries for analysis
import pandas as pd
import numpy as np
from scipy. optimize import curve_fit
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
from index import CPI_df, currency
from conversion import winsorize
from wrangle import alk, pem, iea_alk, iea_pem
import warnings
from electrolyzer_scaling import power_law, learning_rate_visualization
warnings.filterwarnings("ignore")

# Define an exponential function
def func(x, a, b):
    return a * np.exp(x*b)

def combined_curvefit(db1, db2, x_input, y_input, db1_name, db2_name, a, b, lower = 0.05, upper = 0.95, file_name=None):
    fig = plt.figure(figsize=(16, 5))
    sns.set_theme(style="white")
    plt.grid(linestyle = "dashed", linewidth = 1)
    plt.xlabel(x_input, fontsize = 20, fontweight = "bold")
    plt.ylabel(y_input, fontsize = 20, fontweight = "bold")
    plt.title(f"Single Curve fitting result for {db1_name} and {db2_name}", fontsize = 18, fontweight = "bold")

    colors = [(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)]
    
    fitted_values = {} 
    
    for db, db_name, color in zip([db1, db2], [db1_name, db2_name], colors):
        df = winsorize(db, y_input, lower, upper)
        x = df[x_input]
        y = df[y_input]
        popt, pcov = curve_fit(func, x, y, p0 = (a, b), maxfev = 1000000, method = "lm")
        if popt[1] < 0:
            rate_type = 'Decline'
        else:
            rate_type = 'Incline'
        print(f"The {rate_type} Rate for {db_name}= {popt[1]*100 :.2f}%")

        x_values = range(1992, 2051, 1)
        y_values = func(x_values, *popt)
        
        fitted_values[db_name] = y_values # store y_values in dictionary
        
        y_err = np.std(func(x_values, *popt))
        y_plus   = y_values + y_err
        y_minus  = np.where((y_values - y_err) < 0, 0, (y_values - y_err))
        y_values_r = func(x, *popt)
        R2 = r2_score( y , y_values_r)

        print(f"The R2 score for {db_name}= {R2 :.2f}")

        sns.scatterplot(x = x, y = y , s = 100, alpha = 0.6, color = color, legend=False)
        sns.lineplot(x= x_values, y = y_values, linewidth = 1.5, color = color, label=db_name)
        plt.fill_between(x_values, y_plus, y_minus, alpha=0.2, color = color)

    plt.xticks(range(1992, 2051, 1), range(1992, 2051, 1), rotation=90, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.legend(fontsize = 20)

    plt.savefig(file_name, dpi=300, bbox_inches='tight')

    return fitted_values  # return the dictionary of y_values

# Cost Reduction Based on Time
cost_singlef = combined_curvefit(alk, pem, x_input = "year_of_estimate", y_input = "cost_2021USD/kW", 
                                       db1_name = "Alkaline", db2_name = "PEM", 
                                       a = 3000, b = -1e-3, file_name = "figures/cost_singlef")
alk_singlef = cost_singlef["Alkaline"]
pem_singlef = cost_singlef["PEM"]

eff_singlef = combined_curvefit(alk, pem, x_input = "year_of_estimate", y_input = "efficiency_LHV", 
                                             db1_name = "Alkaline", db2_name = "PEM",
                                             a = 3000, b = -1e-3, lower = 0, upper = 1, file_name = "figures/eff_singlef")

sys_singlef = combined_curvefit(alk, pem, x_input= "year_of_estimate", y_input= "system_size_kW",
                                db1_name = "Alkaline", db2_name = "PEM",
                                a = 3000, b = -1e-3, lower = 0, upper = 1, file_name = "figures/sys_singlef")


cap_singlef = combined_curvefit(iea_alk, iea_pem, x_input= "date_online", y_input= "normalized_capacity_Mwel",
                                db1_name = "Alkaline", db2_name = "PEM",
                                a = 1, b = 1e-3, lower = 0, upper = 1, file_name = "figures/cap_singlef")



# Cost Reduction based on Scaling Factor
alk_sys = winsorize(alk, "system_size_kW", 0.05, 0.95)
pem_sys = winsorize(pem, "system_size_kW", 0.05, 0.95)
scaling_alk, scaling_pem = learning_rate_visualization("system_size_kW", "cost_2021USD/kW", alk_sys, pem_sys,
                                                                   "System Size vs. Cost", "figures/sys_vs_cost")
alk_singlef_s = power_law(sys_singlef["Alkaline"]/sys_singlef["Alkaline"][0], alk_singlef, -scaling_alk)
pem_singlef_s = power_law(sys_singlef["PEM"]/sys_singlef["PEM"][0], pem_singlef, -scaling_pem)



# Cost Reduction based on technology learning
alk_dict = {"year": range(1992, 2051, 1), "cost_2021USD/kW": alk_singlef}
alk_db = pd.DataFrame.from_dict(alk_dict)
alk_df = pd.merge(alk_db, iea_alk[["date_online","cumulative_capacity_MWel"]], left_on = "year", right_on = "date_online")
alk_df.drop(columns = "date_online", inplace = True)
pem_dict = {"year": range(1992, 2051, 1), "cost_2021USD/kW": pem_singlef}
pem_db = pd.DataFrame.from_dict(pem_dict)
pem_df = pd.merge(pem_db, iea_pem[["date_online","cumulative_capacity_MWel"]], left_on = "year", right_on = "date_online")
pem_df.drop(columns = "date_online", inplace = True)
learning_alk, learning_pem = learning_rate_visualization("cumulative_capacity_MWel", "cost_2021USD/kW", alk_df, pem_df,
                                                         "Installed Capacity vs. Cost (Single)", "figures/capacity_vs_cost")


alk_singlef_l = power_law(cap_singlef["Alkaline"].cumsum()/cap_singlef["Alkaline"].cumsum()[0], alk_singlef, -learning_alk)
pem_singlef_l = power_law(cap_singlef["PEM"].cumsum()/cap_singlef["PEM"].cumsum()[0], pem_singlef, -learning_pem)



# Cost Reduction Based on Scaling + Learning
alk_singlef_sl = power_law(cap_singlef["Alkaline"]/cap_singlef["Alkaline"][0], alk_singlef_s, -learning_alk)
pem_singlef_sl = power_law(cap_singlef["PEM"]/cap_singlef["PEM"][0], pem_singlef_s, -learning_pem)

