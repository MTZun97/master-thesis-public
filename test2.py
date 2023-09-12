from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from oxygen import cash_flow
import dash
from carbontax import create_carbontax_plot

# Initialize Dash app
app = dash.Dash(__name__)

block_color = '#f0f0f0'  # Use a light grey background color

# Layout of the app
app.layout = html.Div([
    html.Div([
        html.Span("Carbon Tax Plot Parameters:", style={'font-weight': 'bold'}),
        html.Br(),
        
        html.Div([
            html.Label('NG Price:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='NG_price', type='number', value=30, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('CCUS Percent:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='CCUS_percent', type='number', value=30, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Capture Rate:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='capture_rate', type='number', value=90, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Carbon Tax:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='carbon_tax', type='number', value=350, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electricity Price CO2 Start:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electricity_price_CO2_start', type='number', value=0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),

        html.Div([
            html.Label('Electricity Price CO2 End:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electricity_price_CO2_end', type='number', value=0.11, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),

        html.Div([
            html.Label('Electrolyzer Efficiency CO2:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electrolyzer_efficiency_CO2', type='number', value=70, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),

        html.Div([
            html.Label('Electrolyzer Cost CO2:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electrolyzer_cost_CO2', type='number', value=1000, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),

        html.Div([
            html.Label('Capacity Factor CO2:', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='capacity_factor_CO2', type='number', value=0.6, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
    ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top', 'padding': '5px', 'margin': '10px', 'background-color': block_color}),
    
    dcc.Graph(id='carbon_tax_plot', style={'display': 'inline-block', 'width': '65%', 'vertical-align': 'top',  'padding': '5px', 'margin': '10px', 'background-color': block_color }),
])

# Here, you would insert the definition of the create_carbontax_plot function and the callback function to update the graph based on the inputs.

# Callback to update graph based on inputs
@app.callback(
    Output('carbon_tax_plot', 'figure'),
    [
        Input('NG_price', 'value'),
        Input('CCUS_percent', 'value'),
        Input('capture_rate', 'value'),
        Input('carbon_tax', 'value'),
        Input('electricity_price_CO2_start', 'value'),
        Input('electricity_price_CO2_end', 'value'),
        Input('electrolyzer_efficiency_CO2', 'value'),
        Input('electrolyzer_cost_CO2', 'value'),
        Input('capacity_factor_CO2', 'value'),
    ]
)
def update_graph(NG_price, CCUS_percent, capture_rate, carbon_tax, electricity_price_CO2_start, 
                 electricity_price_CO2_end, electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, 
                 capacity_factor_CO2):

    return create_carbontax_plot(NG_price, CCUS_percent, capture_rate, carbon_tax, 
        [electricity_price_CO2_start, electricity_price_CO2_end], 
        electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, capacity_factor_CO2
    )


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
