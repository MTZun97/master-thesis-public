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
import pandas as pd
from index import CPI_df, currency
from conversion import calc_new_efficiency, calc_new_sys_size, get_country_name

iea_data = pd.read_excel("excel/Reference.xlsx", header = 0, sheet_name = "iea_project")
iea_data = iea_data[(iea_data["product"] == "H2") ]
iea_data = iea_data[(iea_data["technology"] == "ALK") | (iea_data["technology"] == "PEM") | 
                    (iea_data["technology"] == "SOEC") | (iea_data["technology"] == "Other Electrolysis")]
iea_data = iea_data[iea_data["announced_size"].notnull()]
iea_data.drop(columns = [ "normalized_capacity_nm2H2/h", "product", "normalized_capacity_ktH2/y"], inplace = True)
iea_data = iea_data[iea_data["country"].notnull()]
iea_data["country"] = [c[:3] for c in iea_data["country"]]
# apply the function to the ISO3 column and store the result in a new column
iea_data['country_converted'] = iea_data['country'].apply(get_country_name)

iea_alk = pd.DataFrame(iea_data[(iea_data["technology"] == "ALK")].groupby("date_online")["normalized_capacity_Mwel"].sum())[1992:].reset_index()
iea_pem = pd.DataFrame(iea_data[(iea_data["technology"] == "PEM")].groupby("date_online")["normalized_capacity_Mwel"].sum()).reset_index()


# Define an exponential function
def func(x, a, b):
    return a * np.exp(x*b)

def combined_curvefit(db1, db2, x_input, y_input, db1_name, db2_name, a, b, lower = 0.05, upper = 0.95, file_name=None, log = False):
    fig = plt.figure(figsize=(16, 5))
    sns.set_theme(style="white")
    plt.grid(linestyle = "dashed", linewidth = 1)
    plt.xlabel(x_input, fontsize = 16, fontweight = "bold")
    plt.ylabel(y_input, fontsize = 16, fontweight = "bold")
    plt.title(f"Combined Curve fitting result for {db1_name} and {db2_name}", fontsize = 18, fontweight = "bold")

    colors = [(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)]
    
    fitted_values = {} 
    
    for db, db_name, color in zip([db1, db2], [db1_name, db2_name], colors):
        df = winsorize(db, y_input, lower, upper)
        x = df[x_input]
        if log:
            y = np.log(df[y_input]*1000)
        else:
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
        if log:
            plt.ylabel("cumulative_capacity_kWel[log]")

    plt.xticks(range(1992, 2051, 1), range(1992, 2051, 1), rotation=90, fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    plt.legend()

    plt.savefig(file_name, dpi=300, bbox_inches='tight')

    return fitted_values  # return the dictionary of y_values


cap_singlef = combined_curvefit(iea_alk, iea_pem, x_input= "date_online", y_input= "normalized_capacity_Mwel",
                                db1_name = "Alkaline", db2_name = "PEM",
                                a = 10, b = 1e-3, lower = 0, upper = 1, file_name = "figures/cap_singlef")


