import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from oxygen import create_O2revenue_plot

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('ASU Cost', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='ASU_cost', type='number', value=200, min=0, step=5, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electricity Price', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='electricity_price', type='number', value=0.036, min=0.01, step=0.001, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electrolyzer Efficiency', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='electrolyzer_efficiency', type='number', value=70, min=0, max=100, step=1, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electrolyzer Cost', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='electrolyzer_cost', type='number', value=1000, min=0, step=5, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Capacity Factor', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='capacity_factor', type='number', value=0.6, min=0, max=1, step=0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Natural Gas Price', style={'display': 'inline-block', 'width': '300px'}),
            dcc.Input(id='NG_price', type='number', value=10, min=0, step=1, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        

        html.Div([
            html.Label('O2 Price Range', style={'display': 'inline-block', 'width': '300px'}),
            dcc.RangeSlider(
                id='O2_price_slider',
                min=0,
                max=7,
                value=[0, 5],
                step=0.5,
            ),
        ], style={'margin-bottom': '10px'}),
    ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top', 'padding': '5px', 'margin': '10px', 'background-color': '#f9f9f9'}),
    
    dcc.Graph(id='line_plot', style={'display': 'inline-block', 'width': '65%', 'vertical-align': 'top',  'padding': '5px', 'margin': '10px', 'background-color': '#f9f9f9' }),
])

# Callback function to update the plot based on input values
@app.callback(
    Output('line_plot', 'figure'),
    [
        Input('ASU_cost', 'value'),
        Input('electricity_price', 'value'),
        Input('electrolyzer_efficiency', 'value'),
        Input('electrolyzer_cost', 'value'),
        Input('capacity_factor', 'value'),
        Input('NG_price', 'value'),
        Input('O2_price_slider', 'value')
    ]
)
def update_plot( ASU_cost, electricity_price, electrolyzer_efficiency, electrolyzer_cost, capacity_factor, NG_price, O2_price):
    return create_O2revenue_plot( ASU_cost, electricity_price, electrolyzer_efficiency, electrolyzer_cost, capacity_factor, NG_price, O2_price)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
