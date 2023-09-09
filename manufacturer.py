import pandas as pd
import plotly.express as px
import pycountry


def get_country_name(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code).name
    except:
        return 'Unknown'


def manufacturer_count():
    filepath = 'data/Reference.xlsx'
    manufacturer_data = pd.read_excel(
        filepath, header=0, sheet_name="manufacturer")

    # manufacturer_data['headquarter'] = manufacturer_data['headquarter'].apply(get_country_name)
    manufacturer_data['headquarter'] = manufacturer_data['headquarter']

    total_counts = manufacturer_data.groupby(
        ['headquarter', 'technology']).size().unstack(fill_value=0).reset_index()

    fig = px.bar(total_counts, x='headquarter', y=['Alkaline', 'PEM', 'SOEC'],
                 labels={'headquarter': 'Countries'},
                 category_orders={
                     "headquarter": total_counts['headquarter'].tolist()})

    fig.update_layout(
        xaxis_title_font=dict(size=16),
        yaxis_title_font=dict(size=16),
        xaxis=dict(tickangle=90, tickfont=dict(size=12)),
        yaxis=dict(tickfont=dict(size=12)),
        legend=dict(xanchor="right", x=0.99, yanchor="top", y=0.99),
        showlegend=True,
        plot_bgcolor="#E6E6FA",  # Greyish-blue color
        title_text="<b>Electrolyzer Manufacturers by Country</b>",
        title_x=0.5,  # Center-align the title horizontally
        title_font=dict(size=18, family='Arial', color='black'),
        margin=dict(b=50)  # Adjust the 'b' margin value to your preference
    )

    return fig
