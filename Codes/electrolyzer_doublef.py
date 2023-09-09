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
import random
from sklearn.metrics import mean_absolute_error
from electrolyzer_scaling import power_law, learning_rate_visualization
from electrolyzer_singlef import scaling_alk, scaling_pem, learning_alk, learning_pem, sys_singlef, cap_singlef
warnings.filterwarnings("ignore")

# Define an exponential function
def func(x, a, b):
    return a * np.exp(x*b)

alk_cost = winsorize(alk, "cost_2021USD/kW", 0.05, 0.95)
pem_cost = winsorize(pem, "cost_2021USD/kW",0.05, 0.95)

# Define Training & Validation data
def train_test(db):
    training = db[db["year_of_estimate"] < 2018][["year_of_estimate", "cost_2021USD/kW"]]
    validation =  db[(db["year_of_estimate"] >= 2018) & (db["method"]=="Manufacturer")][["year_of_estimate", "cost_2021USD/kW"]]
    return training, validation
alk_training, alk_validation = train_test(alk_cost)
pem_training, pem_validation = train_test(pem_cost)

# Visualize Training and Testing data for alkaline electrolyzers
fig = plt.figure(figsize = (16,5))
sns.set_theme(style = "white")
sns.scatterplot(x = "year_of_estimate", y = "cost_2021USD/kW", data = pem_training, alpha = 0.8, s = 100, color = "g", label = "Training set")
sns.scatterplot(x = "year_of_estimate", y = "cost_2021USD/kW", data = pem_validation, alpha = 0.8, s = 100, color = "r", label = "Validation Set")
plt.xticks(range(1990, 2031, 1), range(1990, 2031, 1), rotation=90, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.xlabel("Year of Estimate", fontsize = 20, fontweight = "bold")
plt.ylabel("Cost 2021 USD", fontsize = 20, fontweight = "bold")
plt.grid(linestyle="dashed", linewidth=1, alpha = 0.6)
plt.legend(fontsize = 20)
plt.savefig("figures/training_validation", dpi = 300, bbox_inches = "tight")


# define function to generate a figure
def generate_figure():
    fig = plt.figure(figsize=(16, 5))
    plt.grid(linestyle = "dashed", linewidth = 1)
    return fig

# modify double_curvefit to accept a figure as an argument
def double_curvefit(training, validation, db, x_input, y_input, db_name, a , b, fig, color):
    cost_year = training.groupby(x_input)[y_input].apply(list)
    random.seed(42)
    sets = {}
    for i in range(1000):
        empty_list = []
        for year in cost_year.index:
            empty_list.append(random.choice(cost_year[year]))
        sets[i] = empty_list
    sets_df = pd.DataFrame(sets, index = cost_year.index)
    
    mae = {}
    for i in sets_df.columns:
        x = sets_df[i].index
        y = sets_df[i]
        popt, pcov = curve_fit(func, x, y, p0 = (a, b), maxfev = 10000, method = "lm")
        mae[i] = mean_absolute_error(validation[y_input], func(validation[y_input], *popt))
    
    mae_df = pd.DataFrame(list(mae.items()))
    mae_df = mae_df.drop(columns = [0]).rename(columns = {1 : "value"})
    mae_df["rank"] = mae_df["value"].rank(ascending = False)
    mae_df["weight"] = mae_df["rank"]/sum(mae_df["rank"])
    
    for i in sets_df.columns:
        sets_df[i] = sets_df[i]*mae_df["weight"][i]
    
    sets_df["sum"] = sets_df.sum(axis = 1)
    
    x = sets_df.index
    y = sets_df["sum"]
    popt_s, pcov = curve_fit(func, x , y, p0 = (a, b), maxfev = 1000000, method = "lm")
    if popt[1] < 0:
        rate_type = 'Decline'
    else:
        rate_type = 'Incline'
    print(f"The {rate_type} Rate for {db_name}= {popt[1]*100 :.2f}%")
    
    x_values = range(1992, 2051, 1)
    y_values = func(x_values, *popt)
    y_values_r = func(x, *popt)
    R2 = r2_score( y , y_values_r)

    print("Correlation R2 = ", R2)
    y_err = np.std(func(x_values, *popt))
    y_plus   = y_values + y_err
    y_minus  = np.where((y_values - y_err) < 0, 0, (y_values - y_err))
    #plotting the curve
    sns.set_theme(style="white")
    sns.scatterplot(x = db[x_input], y = db[y_input] , s = 100, alpha = 0.6, color = color, ax=fig.axes[0])
    sns.lineplot(x= x_values, y = y_values, linewidth = 1.5, color = color, ax=fig.axes[0], label = db_name)
    plt.fill_between(x_values, y_plus, y_minus, alpha=0.2)
    plt.xticks(x_values, x_values, rotation=90, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.xlabel(x_input, fontsize = 20, fontweight = "bold")
    plt.ylabel(y_input, fontsize = 20, fontweight = "bold")
    plt.legend(fontsize = 20)
    plt.title(f"Double Curve fitting result for {db_name}", fontsize = 18, fontweight = "bold")
    return y_values

# now you can generate a figure and plot both data sets on it
fig = generate_figure()
alk_doublef= double_curvefit(training = alk_training, validation =  alk_validation, db = alk_cost, x_input = "year_of_estimate",
                             y_input = "cost_2021USD/kW", db_name = "Alkaline", a = 3000, b = -1e-2,
                             fig = fig, color = "r")

pem_doublef = double_curvefit(training = pem_training, validation =  pem_validation, db = pem_cost, x_input = "year_of_estimate",
                             y_input = "cost_2021USD/kW", db_name = "PEM", a = 3000, b = -1e-2,
                             fig = fig, color = "b")
plt.savefig("figures/cost_doublef", dpi=300, bbox_inches='tight')

# Cost Reduction based on technology learning
alk_dict = {"year": range(1992, 2051, 1), "cost_2021USD/kW": alk_doublef}
alk_db = pd.DataFrame.from_dict(alk_dict)
alk_df = pd.merge(alk_db, iea_alk[["date_online","cumulative_capacity_MWel"]], left_on = "year", right_on = "date_online")
alk_df.drop(columns = "date_online", inplace = True)
pem_dict = {"year": range(1992, 2051, 1), "cost_2021USD/kW": pem_doublef}
pem_db = pd.DataFrame.from_dict(pem_dict)
pem_df = pd.merge(pem_db, iea_pem[["date_online","cumulative_capacity_MWel"]], left_on = "year", right_on = "date_online")
pem_df.drop(columns = "date_online", inplace = True)
learning_alk_double, learning_pem_double = learning_rate_visualization("cumulative_capacity_MWel", "cost_2021USD/kW", alk_df, pem_df,
                                                         "Installed Capacity vs. Cost (Double)", "figures/capacity_vs_cost_double")


# Cost Reduction based on Scaling Factor
alk_doublef_s = power_law(sys_singlef["Alkaline"]/sys_singlef["Alkaline"][0], alk_doublef, -scaling_alk)
pem_doublef_s = power_law(sys_singlef["PEM"]/sys_singlef["PEM"][0], pem_doublef, -scaling_pem)

# Cost Reduction based on technology learning
alk_doublef_l = power_law(cap_singlef["Alkaline"].cumsum()/cap_singlef["Alkaline"].cumsum()[0], alk_doublef, -learning_alk_double)
pem_doublef_l = power_law(cap_singlef["PEM"].cumsum()/cap_singlef["PEM"].cumsum()[0], pem_doublef, -learning_pem_double)

# Cost Reduction Based on Scaling + Learning
alk_doublef_sl = power_law(cap_singlef["Alkaline"].cumsum()/cap_singlef["Alkaline"].cumsum()[0], alk_doublef_s, -learning_alk)
pem_doublef_sl = power_law(cap_singlef["PEM"].cumsum()/cap_singlef["PEM"].cumsum()[0], pem_doublef_s, -learning_pem)
