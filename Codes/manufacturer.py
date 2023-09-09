from wrangle import manufacturer_data
import matplotlib.pyplot as plt
import seaborn as sns

total_counts = manufacturer_data.groupby('headquarter')['technology'].value_counts().unstack().fillna(0).sum(axis=1)
sorted_countries = total_counts.sort_values(ascending=False).index.tolist()

# Plot the stacked countplot
ax = plt.figure(figsize=(16, 5))
ax = sns.countplot(x='headquarter', data=manufacturer_data, hue='technology', palette="deep",
                    order=sorted_countries)
ax.set_xlabel('Countries', fontsize=16, fontweight = "bold", font = "Arial")
ax.set_ylabel('Count', fontsize=16, fontweight = "bold", font = "Arial")
ax.set_title('Count of Electrolyzers Manufacturing Companies per country', fontsize=18, fontweight = "bold", font = "Arial")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=12, fontweight = "bold", font = "Arial")
plt.yticks(fontsize = 12, fontweight = "bold", font = "Arial")
plt.grid(linestyle='dashed', linewidth=1)
plt.legend(loc='upper right')
plt.savefig("figures/manufacturer.png", dpi=300, bbox_inches="tight")