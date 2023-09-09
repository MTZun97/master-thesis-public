from wrangle import alk, pem, soec
from conversion import winsorize
import matplotlib.pyplot as plt
import seaborn as sns

def scatterplot(df, x, y, hue, file_name = None):
  fig = plt.figure(figsize = (16,5))
  sns.set_theme(style = "white")
  sns.scatterplot(x = df[x], y = df[y], data = df, hue = hue, alpha = 0.8, s = 100, palette = "deep") 
  plt.xticks(range(1990, 2051, 1), range(1990, 2051, 1), rotation=90, fontsize=12, fontweight='bold')
  plt.yticks(fontsize=12, fontweight='bold')
  plt.xlabel(x, fontsize = 20, fontweight = "bold")
  plt.ylabel(y, fontsize = 20, fontweight = "bold")
  plt.grid(linestyle="dashed", linewidth=1, alpha = 0.6)
  plt.legend(fontsize = 20)
  plt.savefig(file_name, dpi = 300, bbox_inches = "tight")

#Original Data
# Cost Visualization
for df,name in zip([alk, pem, soec], ["figures/alk_cost", "figures/pem_cost", "figures/soec_cost"]):
    scatterplot(df, "year_of_estimate", y = "cost_2021USD/kW", hue = "method", file_name = name)
    
# Efficiency Visualization
for df,name in zip([alk, pem, soec], ["figures/alk_eff", "figures/pem_eff", "figures/soec_eff"]):
    scatterplot(df, "year_of_estimate", y = "efficiency_LHV", hue = "method", file_name = name)
    
# System Size Visualization
for df,name in zip([alk, pem, soec], ["figures/alk_size", "figures/pem_size", "figures/soec_size"]):
    scatterplot(df, "year_of_estimate", y = "system_size_kW", hue = "method", file_name = name)
    
    
#Winsorized Data
#Cost Visualization
for df,name in zip([alk, pem, soec], ["figures/alk_cost_winsorized", "figures/pem_cost_winsorized", "figures/soec_cost_winsorized"]):
    df_winsorized = winsorize(alk, "cost_2021USD/kW", 0.05, 0.95)
    scatterplot(df_winsorized, "year_of_estimate", y = "cost_2021USD/kW", hue = "method", file_name = name)
    
#System Size Visualization
for df,name in zip([alk, pem, soec], ["figures/alk_size_winsorized", "figures/pem_size_winsorized", "figures/soec_size_winsorized"]):
    df_winsorized = winsorize(alk, "system_size_kW", 0.05, 0.95)
    scatterplot(df_winsorized, "year_of_estimate", y = "system_size_kW", hue = "method", file_name = name)
    