import plotly.express as px
import pandas as pd


def plot_cost_reduction(method):

    data = pd.read_csv("data/cost_reduction.csv", index_col=0)
    alk_singlef_data = data[["alk_singlef",
                             "alk_singlef_s", "alk_singlef_l", "alk_singlef_sl"]]
    pem_singlef_data = data[["pem_singlef",
                             "pem_singlef_s", "pem_singlef_l", "pem_singlef_sl"]]
    alk_doublef_data = data[["alk_doublef",
                             "alk_doublef_s", "alk_doublef_l", "alk_doublef_sl"]]
    pem_doublef_data = data[["pem_doublef",
                             "pem_doublef_s", "pem_doublef_l", "pem_doublef_sl"]]

    if method == "Single":
        alk_data = alk_singlef_data
        pem_data = pem_singlef_data
    elif method == "Double":
        alk_data = alk_doublef_data
        pem_data = pem_doublef_data

    fig = px.line()

    line_styles = ['dot', 'dash', 'dashdot', 'solid']
    colors = ['#c43932', '#4c72b0'] 
    labels = ["time", "time+scaling", "time+learning", "time+scaling+learning"]

    for j, (data, color, title) in enumerate(zip([alk_data, pem_data], colors, ['Alkaline', 'PEM'])):
        for i, y in enumerate(data.columns):
            style = line_styles[i % len(line_styles)]
            fig.add_scatter(x=data.index, y=data[y], mode='lines',
                            name=f"{title}: {labels[i]}", line=dict(color=color, dash=style))

    fig.update_xaxes(tickvals=list(range(1992, 2051, 1)), ticktext=list(range(1992, 2051, 1)),
                     tickangle=90, tickfont=dict(size=12, family='bold'))
    fig.update_yaxes(tickfont=dict(size=12, family='bold'))
    fig.update_layout(xaxis_title="year", yaxis_title="cost_2021USD",
                      title=f"<b>Cost Reduction Potential for Alkaline and PEM Electrolyzers Through {method} Curve Fitting<b>",
                      title_font=dict(size=18, family='Arial', color='black'),title_x = 0.5,
                      legend=dict(font=dict(size=17),xanchor="right", x=0.99, yanchor="top", y=0.99))
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

    return fig

