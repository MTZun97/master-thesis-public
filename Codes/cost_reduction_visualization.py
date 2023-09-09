import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
from electrolyzer_singlef import eff_singlef
from electrolyzer_singlef import alk_singlef, alk_singlef_s, alk_singlef_l, alk_singlef_sl
from electrolyzer_singlef import pem_singlef, pem_singlef_s, pem_singlef_l, pem_singlef_sl
from electrolyzer_doublef import alk_doublef, alk_doublef_s, alk_doublef_l, alk_doublef_sl
from electrolyzer_doublef import pem_doublef, pem_doublef_s, pem_doublef_l, pem_doublef_sl

def plot_cost_reduction(alk_data, pem_data, method, filename):
    plt.figure(figsize=(16, 5))
    sns.set_theme(style="white")
    line_styles = [':', '--', '-.', '-']
    colors = [(0.7686274509803922, 0.3058823529411765, 0.3215686274509804), 
              (0.2980392156862745, 0.4470588235294118, 0.6901960784313725)]
    labels = ["time", "time+scaling", "time+learning", "time+scaling+learning"]
    
    for j, (data, color, title) in enumerate(zip([alk_data, pem_data], colors, ['Alkaline', 'PEM'])):
        for i, y in enumerate(data):
            style = line_styles[i % len(line_styles)]
            sns.lineplot(x=range(1992, 2051, 1), y=y, linewidth=2, linestyle=style, color=color, label=f"{title}: {labels[i]}")
    
    plt.xticks(range(1992, 2051, 1), range(1992, 2051, 1), rotation=90, fontsize=12, fontweight="bold")
    plt.yticks(fontsize=12, fontweight="bold")
    plt.grid(linestyle="dashed", linewidth=1) 
    plt.xlabel("year", fontsize=16, fontweight="bold")  
    plt.ylabel("cost_2021USD", fontsize=16, fontweight="bold")
    plt.title(f"Cost Reduction Potential for Alkaline and PEM Electrolyzers Through {method} Curve Fitting", fontsize=18, fontweight="bold")
    plt.legend(fontsize = 17)
    plt.savefig(f"figures/{filename}", dpi=600, bbox_inches='tight')
    plt.close()

alk_singlef_data = [alk_singlef, alk_singlef_s, alk_singlef_l, alk_singlef_sl]
pem_singlef_data = [pem_singlef, pem_singlef_s, pem_singlef_l, pem_singlef_sl]
alk_doublef_data = [alk_doublef, alk_doublef_s, alk_doublef_l, alk_doublef_sl]
pem_doublef_data = [pem_doublef, pem_doublef_s, pem_doublef_l, pem_doublef_sl]

plot_cost_reduction(alk_singlef_data, pem_singlef_data, "Single", "cost_reduction_singlef")
plot_cost_reduction(alk_doublef_data, pem_doublef_data, "Double", "cost_reduction_doublef")


# list of your data
data = [eff_singlef["Alkaline"], eff_singlef["PEM"], alk_singlef, alk_singlef_s, alk_singlef_l, alk_singlef_sl,
        pem_singlef, pem_singlef_s, pem_singlef_l, pem_singlef_sl,
        alk_doublef, alk_doublef_s, alk_doublef_l, alk_doublef_sl,
        pem_doublef, pem_doublef_s, pem_doublef_l, pem_doublef_sl]

# list of column names
columns = ["eff_singlef_alk", "eff_singlef_pem", "alk_singlef", "alk_singlef_s", "alk_singlef_l", "alk_singlef_sl",
           "pem_singlef", "pem_singlef_s", "pem_singlef_l", "pem_singlef_sl",
           "alk_doublef", "alk_doublef_s", "alk_doublef_l", "alk_doublef_sl",
           "pem_doublef", "pem_doublef_s", "pem_doublef_l", "pem_doublef_sl"]

# Create DataFrame
df = pd.DataFrame(data, index=columns).T

# set your index range
df.index = range(1992, 2051, 1)

# Save to CSV
df.to_csv("excel/cost_reduction.csv")

