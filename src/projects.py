import plotly.express as px
import pandas as pd
import pycountry
import os


def project_count():
    filepath = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "data", "Reference.xlsx")
    )
    iea_data = pd.read_excel(filepath, header=0, sheet_name="iea_project")
    iea_data = iea_data[(iea_data["product"] == "H2")]
    iea_data = iea_data[
        (iea_data["technology"] == "ALK")
        | (iea_data["technology"] == "PEM")
        | (iea_data["technology"] == "SOEC")
        | (iea_data["technology"] == "Other Electrolysis")
    ]
    iea_data = iea_data[iea_data["announced_size"].notnull()]
    iea_data.drop(
        columns=[
            "normalized_capacity_nm2H2/h",
            "product",
            "normalized_capacity_ktH2/y",
        ],
        inplace=True,
    )
    iea_data = iea_data[iea_data["country"].notnull()]
    iea_data["country"] = [c[:3] for c in iea_data["country"]]
    iea_data["country_converted"] = iea_data["country"]

    grouped_data = (
        iea_data.groupby(["country_converted", "status"])
        .size()
        .reset_index(name="count")
    )

    # Get total count per country
    total_count = (
        grouped_data.groupby("country_converted")["count"]
        .sum()
        .reset_index(name="total_count")
    )

    # Merge total count back to grouped_data
    grouped_data = grouped_data.merge(total_count, on="country_converted", how="left")

    # Sort total_count in descending order
    total_count = total_count.sort_values("total_count", ascending=False)

    fig = px.bar(
        grouped_data,
        x="country_converted",
        y="count",
        color="status",
        category_orders={
            "country_converted": total_count["country_converted"].tolist()
        },
        labels={"country_converted": "Countries", "count": "Count"},
        custom_data=[grouped_data["total_count"]],
    )

    fig.update_traces(
        hovertemplate="Country: %{x}<br>Count: %{y}<br>Total Projects in Country: %{customdata[0]}"
    )

    fig.update_layout(
        yaxis=dict(
            title_text="Number of Projects",
            title_font=dict(family="Arial, bold", size=20),
            tickfont=dict(family="Arial, bold", size=16),
        ),
        xaxis=dict(
            title_text="Countries",
            title_font=dict(family="Arial, bold", size=20),
            tickfont=dict(family="Arial, bold", size=16),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(family="Arial Bold", size=16, color="black"),
            bordercolor="Black",
            borderwidth=2,
            itemsizing="constant",
        ),
        legend_title_text="",
        margin=dict(
            t=50,
        ),
    )

    return fig
