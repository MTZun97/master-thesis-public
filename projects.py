import plotly.express as px
import pandas as pd
import pycountry

def project_count():
    filepath = 'data/Reference.xlsx'
    iea_data = pd.read_excel(filepath, header=0, sheet_name="iea_project")
    iea_data = iea_data[(iea_data["product"] == "H2")]
    iea_data = iea_data[(iea_data["technology"] == "ALK") | (iea_data["technology"] == "PEM") |
                        (iea_data["technology"] == "SOEC") | (iea_data["technology"] == "Other Electrolysis")]
    iea_data = iea_data[iea_data["announced_size"].notnull()]
    iea_data.drop(columns=["normalized_capacity_nm2H2/h",
                  "product", "normalized_capacity_ktH2/y"], inplace=True)
    iea_data = iea_data[iea_data["country"].notnull()]
    iea_data["country"] = [c[:3] for c in iea_data["country"]]
    iea_data['country_converted'] = iea_data['country']

    grouped_data = iea_data.groupby(
        ["country_converted", "status"]).size().reset_index(name="count")
    total_count = grouped_data.groupby("country_converted")[
        "count"].sum().reset_index(name="total_count")
    total_count = total_count.sort_values("total_count", ascending=False)

    fig = px.bar(grouped_data, x="country_converted", y="count", color="status", category_orders={"country_converted": total_count["country_converted"].tolist()},
                 labels={"country_converted": "Countries", "count": "Count"},
                 title="<b>Hydrogen Projects Count per Country<b>")

    fig.update_layout(
        xaxis_title_font=dict(size=16),
        yaxis_title_font=dict(size=16),
        xaxis=dict(tickangle=90, tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        legend=dict(xanchor="right", x=0.99, yanchor="top", y=0.99),
        showlegend=True,
        plot_bgcolor="#E6E6FA",
        title_text="<b>Hydrogen Projects Count per Country</b>",
        title_x=0.5,  
        title_font=dict(size=18, family='Arial', color='black'),
        margin=dict(b=50)  
    )


    return fig

