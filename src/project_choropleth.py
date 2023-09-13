import plotly.express as px
import pandas as pd
import pycountry
import os

def get_country_name(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code).name
    except:
        return 'Unknown'


def generate_choropleth(status="all"):
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "data", "Reference.xlsx"))
    iea_data = pd.read_excel(filepath, header=0, sheet_name="iea_project")
    iea_data = iea_data[(iea_data["product"] == "H2")]
    iea_data = iea_data[(iea_data["technology"] == "ALK") | (iea_data["technology"] == "PEM") |
                        (iea_data["technology"] == "SOEC") | (iea_data["technology"] == "Other Electrolysis")]
    iea_data = iea_data[iea_data["announced_size"].notnull()]
    iea_data.drop(columns=["normalized_capacity_nm2H2/h",
                  "product", "normalized_capacity_ktH2/y"], inplace=True)
    iea_data = iea_data[iea_data["country"].notnull()]
    iea_data["country"] = [c[:3] for c in iea_data["country"]]

    iea_data['country_converted'] = iea_data['country'].apply(get_country_name)

    if status != "all":
        grouped_country = iea_data.groupby(
            ['country', 'status']).sum().reset_index()
        df = grouped_country[grouped_country['status'] == status]
    else:
        df = iea_data

    country_names = df.groupby(['country']).sum(
        numeric_only=True).reset_index()

    country_names['country_count'] = country_names['country'].apply(
        get_country_name)
    value = "normalized_capacity_Mwel"

    hover_template = "<b>%{customdata[0]}</b><br>" + \
                     "Capacity: %{customdata[1]:.2f} MWel/y"

    fig = px.choropleth(country_names,
                        locations="country",
                        color="normalized_capacity_Mwel",
                        hover_name="country_count",
                        color_continuous_scale='blugrn',
                        range_color=(0, country_names[value].max()),
                        custom_data=[country_names['country'],
                                     country_names['normalized_capacity_Mwel']]
                        )
    
    fig.update_coloraxes(colorbar_title='<b>' +
                         value.replace("normalized_capacity_Mwel", "") + "MWel/y" + '</b>')
    title = f"Total Current and Projected Installed Capacity per Country [Status - {status}]"
    if title:
        fig.update_layout(title_text='<b>' + title + '</b>',
                          title_x=0.5,
                          title_font=dict(family="Helvetica Neue, Arial", size=24, color='black'))

    fig.update_layout(margin=dict(l=10, r=10, t=50, b=50))

    fig.update_geos(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )

    fig.update_coloraxes(
        colorbar=dict(
            title=dict(
                text='<b>' +
                value.replace("normalized_capacity_Mwel", "") +
                "MWel/y" + '</b>',
                font=dict(
                    family="Helvetica Neue, Arial",
                    size=16,
                    color='black'
                )
            ),
            thicknessmode="pixels",
            thickness=20,
            lenmode="pixels",
            len=400,
            yanchor='top',
            y=0.85,
            tickfont=dict(size=14),
            x=0.9,
            xanchor='left'
        )
    )

    fig.update_traces(hovertemplate=hover_template)

    return fig

