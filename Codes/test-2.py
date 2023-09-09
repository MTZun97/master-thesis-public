import matplotlib.pyplot as plt
import seaborn as sns
from wrangle import iea_data
from conversion import get_country_name
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

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
    
    fig.update_layout(margin=dict(l=50, r=50, t=50, b=50))  # Increase the top margin
    
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

