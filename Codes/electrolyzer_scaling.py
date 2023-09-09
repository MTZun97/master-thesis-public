from wrangle import alk, pem
import matplotlib.pyplot as plt
import seaborn as sns
from scipy. optimize import curve_fit
from sklearn.metrics import r2_score
from conversion import winsorize

def power_law (x, a, b):
    return a * x**b

def learning_rate(x_input, y_input, db, title):
    x = db[x_input]
    y = db[y_input]
    
    popt, pcov = curve_fit(power_law, x, y, maxfev = 100000)
    
    x_values = x
    y_values = power_law(x_values, *popt)

    R2 = r2_score( y , y_values)
    learning_rate = (1-2**popt[1])
    print(f"The R2 score for {title}= {R2 :.2f}")
    print(f"Scaling effect for {title} = {popt[1]:.2f}")
    print(f"Learning Rate for {title} = {(learning_rate)*100:.2f}%")
    return learning_rate, x, y, x_values, y_values


def learning_rate_visualization(x_input, y_input, alk_data, pem_data, title, file_name):
    learning_rate_alk, alk_x, alk_y, alk_xvalues, alk_yvalues = learning_rate(x_input, y_input, alk_data, "ALK" )
    learning_rate_pem, pem_x, pem_y, pem_xvalues, pem_yvalues = learning_rate(x_input, y_input, pem_data, "PEM" )
    
   
    fig = plt.figure(figsize=(16, 5))
    sns.set_theme(style="white")
    
    
    sns.scatterplot(x = alk_x, y = alk_y, s = 100, alpha = 0.7, color = "r", label = "ALK")
    sns.scatterplot(x = pem_x, y = pem_y, s = 100, alpha = 0.7, color = "b", label = "PEM")
    
    sns.lineplot(x= alk_xvalues, y = alk_yvalues, linewidth = 2, color = "r")
    sns.lineplot(x= pem_xvalues, y = pem_yvalues, linewidth = 2, color = "b")
    plt.grid(linestyle = "dashed", linewidth = 1)
    plt.xticks(fontsize = 12, fontweight = "bold")
    plt.yticks(fontsize = 12, fontweight = "bold")
    plt.xscale("log")   
    plt.xlabel(x_input, fontsize = 16, fontweight = "bold")
    plt.ylabel(y_input, fontsize = 16, fontweight = "bold")
    plt.title(f"{title}", fontsize = 18, fontweight = "bold")
    plt.legend()
    plt.savefig(file_name, dpi=300, bbox_inches='tight')
    return learning_rate_alk, learning_rate_pem

