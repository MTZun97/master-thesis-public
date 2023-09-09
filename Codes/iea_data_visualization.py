import matplotlib.pyplot as plt
import seaborn as sns
from wrangle import iea_data
from conversion import get_country_name
import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

# Visualization for project counts
def barplot(df, x_col, title, hue = None, file_name=None):
    sns.set(style="white")
    count_df = df[x_col].value_counts().reset_index().rename(columns={x_col: "count", "index": x_col})
    count_df = count_df.sort_values(by="count", ascending=False)
    ax = plt.figure(figsize=(16,5))
    ax = sns.barplot(x=x_col, y="count", data=count_df, palette="deep", order=count_df[x_col])
    ax.set_xlabel("Status", fontsize=16, fontweight = "bold")
    ax.set_ylabel("Count", fontsize=16, fontweight = "bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize = 12, fontweight = "bold")
    plt.yticks(fontsize=12, fontweight='bold')
    plt.grid(linestyle="dashed", linewidth=1)
    plt.title(title, fontsize = 18, fontweight = "bold")
    plt.ylim(0,350)
    gap = 1
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2.,
                height + gap,
                int(height),
                ha='center',
                fontsize = 14) 

    plt.savefig(file_name, dpi=300, bbox_inches="tight")
barplot(df = iea_data, x_col = "status", title = "Count of Hydrogen Project", file_name = "figures/status_count")

def plot_hydrogen_project_count(df, file_name = None):
    count = df["country_converted"].value_counts()
    df["country_count"] = df["country_converted"].apply(lambda x: "Others" if count.loc[x] < 10 else x)
    sns.set(style="white")

    # calculate total count for each country and sort dataframe by total count
    total_count = df.groupby("country_count").size().reset_index(name="total_count")
    total_count = total_count.sort_values("total_count", ascending=False)
    # plot countplot using sorted dataframe
    ax = plt.figure(figsize = (16,5))
    ax = sns.countplot(x="country_count", data=df, hue = "status", order=total_count["country_count"], palette = "deep")
    ax.set_xlabel("Countries", fontsize=16, fontweight = "bold")
    ax.set_ylabel("Count", fontsize=16, fontweight = "bold")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize = 12, fontweight = "bold")
    plt.title("Hydrogen Projects Count per Country", fontsize = 18, fontweight = "bold")
    plt.yticks(fontsize=12, fontweight='bold')
    plt.grid(linestyle = "dashed", linewidth = 1)
    plt.legend(loc="upper right")
    if file_name:
        plt.savefig(file_name, dpi=300, bbox_inches="tight")
plot_hydrogen_project_count(df = iea_data, file_name = "figures/status_count_country")

def generate_choropleth(df, locations, value, hover_name, title=None):
    country_names = df.groupby(['country']).sum().reset_index()
    country_names['country_count'] = country_names['country'].apply(get_country_name)
    
    fig = px.choropleth(country_names, 
                        locations=locations, 
                        color=value,
                        hover_name=hover_name, 
                        color_continuous_scale='blugrn', # change color scale here
                        range_color=(0, country_names[value].max()))
    
    fig.update_coloraxes(colorbar_title='<b>' + value.replace("normalized_capacity_Mwel", "") + "MWel/y" + '</b>')
    
    if title:
        fig.update_layout(title={
            'text': '<b>' + title + '</b>',
            'y': 0.98,  # Adjust the vertical position of the title
            'x': 0.55,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': "Helvetica Neue, Arial",
                'size': 24,
                'color': 'black'
            }
        })
    
    fig.update_layout(margin=dict(l=20, r=50, t=50, b=50))  # Increase the top margin
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text='<b>' + value.replace("normalized_capacity_Mwel", "") + "MWel/y" + '</b>',
                font=dict(
                    family="Helvetica Neue, Arial",
                    size=16,
                    color='black'
                )
            ),
            thicknessmode="pixels",
            thickness=20,
            lenmode="pixels",
            len=400,  # Decrease the length of the scale bar
            yanchor='top',  # Adjust the vertical position of the scale bar
            y=0.98,  # Adjust the vertical position of the scale bar
            tickfont=dict(size=14),  # Increase the scale bar label size
            x=0.92,  # Adjust the horizontal position of the scale bar
            xanchor='left'  # Set the anchor point to the left
        )
    )
    
    fig.show()

generate_choropleth(df = iea_data, locations = "country", value = "normalized_capacity_Mwel",
                    title = "Total Current and Projected Installed Capacity per Country", hover_name =  "country_count")

# Normalized capacity by country and project status
grouped_country = iea_data.groupby(['country', 'status']).sum().reset_index()
for status in grouped_country['status'].unique():
    generate_choropleth(df = grouped_country[grouped_country['status'] == status], locations = "country", 
                        value = "normalized_capacity_Mwel", hover_name =  "country_count", title = f"Total Current and Projected Installed Capacity per Country [Status - {status}]")


#Sankey Diagram
def wrangle_iea(filepath):
    # IEA Database
    iea_data = pd.read_excel(filepath, header=0, sheet_name="iea_project")
    iea_data = iea_data[["source", "technology", "product"]]
    return iea_data

def process_data(df):
    sources = list(df['source'].unique())
    technologies = list(df['technology'].unique())
    products = list(df['product'].unique())

    all_nodes = sources + technologies + products
    node_dict = {node: i for i, node in enumerate(all_nodes)}

    count_data = df.groupby(["source", "technology", "product"]).size().reset_index(name='count')
    count_data[['source_id', 'target_id']] = count_data[['source', 'technology']].applymap(node_dict.get)
    
    second_link = count_data[['technology', 'product', 'count']].copy()
    second_link.columns = ['source', 'target', 'count']
    second_link[['source_id', 'target_id']] = second_link[['source', 'target']].applymap(node_dict.get)
    
    links = pd.concat([count_data, second_link])
    
    # Calculate the total 'count' for each node
    node_values_out = links.groupby("source")['count'].sum()
    node_values_in = links.groupby("target")['count'].sum()
    node_values = node_values_out.add(node_values_in, fill_value=0).astype(int)

    colors = sns.color_palette("muted", len(all_nodes)).as_hex()
    return links, node_dict, node_values, colors



def create_sankey_diagram(links, node_dict, node_values, colors):
    # Convert hex colors to rgba for transparency
    def hex_to_rgba(hex, alpha):
        hex = hex.lstrip('#')
        hlen = len(hex)
        return 'rgba(' + ', '.join([str(int(hex[i:i+hlen//3], 16)) for i in range(0, hlen, hlen//3)]) + ', {})'.format(alpha)

    rgba_colors = [hex_to_rgba(c, 0.5) for c in colors]

    color_link = [rgba_colors[node_dict[src]] for src in links['source']]
    
    fig = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = [f'{node} ({node_values[node]})' for node in node_dict.keys()],
          color = rgba_colors,
        ),
        link = dict(
          source = links['source_id'],
          target = links['target_id'],
          value = links['count'],
          color = color_link,
          hovertemplate = 'Value: %{value}<extra></extra>',
      ))])

    fig.update_layout(title_text="Sankey Diagram from source to product", font=dict(size=30, color='black', family="Arial Black"))
    return fig


def save_figure(fig, path):
    pio.write_html(fig, file=path)

iea_sankey = wrangle_iea("excel/Reference.xlsx")
links, node_dict, node_values, colors = process_data(iea_sankey)
fig = create_sankey_diagram(links, node_dict, node_values, colors)
save_figure(fig, 'figures/sankey.html')


# Capacity Distribution
def scatterplot_iea(df, x, y, hue, marker, file_name = None, ylim = False, legend = True):
  fig = plt.figure(figsize = (16,5))
  sns.set_theme(style = "white")
  sns.scatterplot(x = df[x], y = df[y], data = df, style = marker, hue = hue, alpha = 0.8, s = 100, palette = "deep", legend=legend) 
  plt.xticks(range(1990, 2051, 1), range(1990, 2051, 1), rotation=90, fontsize=12, fontweight='bold')
  plt.yticks(fontsize=12, fontweight='bold')
  if ylim:
    plt.ylim(-300,15000)
  plt.xlabel(x, fontsize = 16, fontweight = "bold")
  plt.ylabel(y, fontsize = 16, fontweight = "bold")
  plt.grid(linestyle="dashed", linewidth=1)
  plt.title("Hydrogen Projects from 1990 to 2050", fontsize = 18, fontweight = "bold")
  plt.savefig(file_name, dpi = 300, bbox_inches = "tight")


iea_capacity = iea_data.dropna(subset = ["date_online"])
iea_capacity["date_online"] = iea_capacity["date_online"].astype(int)
scatterplot_iea(iea_capacity, x = "date_online", y = "normalized_capacity_Mwel",
               hue = "status", marker = "technology", file_name="figures/iea_capacity.png", legend = False)
scatterplot_iea(iea_capacity, x = "date_online", y = "normalized_capacity_Mwel",
               hue = "status", marker = "technology", file_name="figures/iea_capacity_zoom.png", ylim = True, legend = True)
