import pandas as pd
import plotly.express as px
import pycountry
import os

def manufacturer_count():
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "Reference.xlsx"))
    manufacturer_data = pd.read_excel(
        filepath, header=0, sheet_name="manufacturer")
    manufacturer_data['headquarter'] = manufacturer_data['headquarter']

    total_counts = manufacturer_data.groupby(
        ['headquarter', 'technology']).size().unstack(fill_value=0).reset_index()

    fig = px.bar(total_counts, x='headquarter', y=['Alkaline', 'PEM', 'SOEC'],
                 labels={'headquarter': 'Countries'},
                 category_orders={
                     "headquarter": total_counts['headquarter'].tolist()})


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
        legend_title_text=''
    )
    return fig
