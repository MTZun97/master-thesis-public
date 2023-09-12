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
                 labels={"country_converted": "Countries", "count": "Count"})

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
            itemsizing='constant'
        ),
        legend_title_text='',
        width=800,  # Adjust as needed
        height=450  # Adjust as needed
    )


    return fig

