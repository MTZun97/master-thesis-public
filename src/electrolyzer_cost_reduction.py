import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go


def plot_cost_reduction(method):
    csv_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "data", "cost_reduction.csv")
    )

    data = pd.read_csv(csv_file_path, index_col=0)

    alk_singlef_data = data[
        ["alk_singlef", "alk_singlef_s", "alk_singlef_l", "alk_singlef_sl"]
    ]
    pem_singlef_data = data[
        ["pem_singlef", "pem_singlef_s", "pem_singlef_l", "pem_singlef_sl"]
    ]
    alk_doublef_data = data[
        ["alk_doublef", "alk_doublef_s", "alk_doublef_l", "alk_doublef_sl"]
    ]
    pem_doublef_data = data[
        ["pem_doublef", "pem_doublef_s", "pem_doublef_l", "pem_doublef_sl"]
    ]

    if method == "Single":
        alk_data = alk_singlef_data
        pem_data = pem_singlef_data
    elif method == "Double":
        alk_data = alk_doublef_data
        pem_data = pem_doublef_data

    fig = go.Figure()

    line_styles = ["dot", "dash", "dashdot", "solid"]
    colors = ["#636EFA", "#FF6692"]
    labels = ["time", "time+scaling", "time+learning", "time+scaling+learning"]

    for j, (data, color, title) in enumerate(
        zip([alk_data, pem_data], colors, ["Alkaline", "PEM"])
    ):
        for i, y in enumerate(data.columns):
            style = line_styles[i % len(line_styles)]
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[y],
                    mode="lines",
                    name=f"{title}: {labels[i]}",
                    line=dict(color=color, dash=style, width=3),
                    hovertemplate="Year: %{x}<br>Cost: $%{y:.0f}/kW<extra></extra>",  # Format hover data here
                )
            )
    fig.update_xaxes(
        tickvals=list(range(1992, 2051, 2)),
        ticktext=list(range(1992, 2051, 2)),
        tickangle=90,
    )

    fig.update_layout(
        yaxis=dict(
            title_text="Electrolyzer Cost ($/kW)",
            title_font=dict(family="Arial, bold", size=20),
            tickfont=dict(family="Arial, bold", size=16),
        ),
        xaxis=dict(
            title_text="Year of Estimate",
            title_font=dict(family="Arial, bold", size=20),
            tickfont=dict(family="Arial, bold", size=16),
        ),
        legend=dict(font=dict(size=17), xanchor="right", x=0.99, yanchor="top", y=0.99),
    )
    return fig
