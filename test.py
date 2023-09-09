import dash
from dash import html, dcc, Input, Output
import pandas as pd
from lcoh import cash_flow, lcoe, lcoe_constant, valid_sources
import plotly.graph_objects as go
from global_lcoh import capacity_factor, global_lcoh
# Initialize Dash app
app = dash.Dash(__name__)

# ... (Rest of your existing code)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Global Levelized Cost of Hydrogen (LCOH) Calculator"),
    html.Div([
        html.Label("Offshore Wind LCOE:"),
        dcc.Input(id='offshore_wind_lcoe', type='number', value=0.23, step=0.01),
        html.Label("Solar LCOE:"),
        dcc.Input(id='solar_lcoe', type='number', value=0.12, step=0.01),
        html.Label("Onshore Wind LCOE:"),
        dcc.Input(id='onshore_wind_lcoe', type='number', value=0.23, step=0.01),
    ]),
    html.Div([
        html.Label("Electrolyzer Type:"),
        dcc.Dropdown(
            id='electrolyzer_type',
            options=[
                {'label': 'Alkaline', 'value': 'alk'},
                {'label': 'PEM', 'value': 'pem'}
            ],
            value='alk'
        ),
    ]),
    dcc.Graph(id='lcoh_graph')
])

@app.callback(
    Output('lcoh_graph', 'figure'),
    [
        Input('offshore_wind_lcoe', 'value'),
        Input('solar_lcoe', 'value'),
        Input('onshore_wind_lcoe', 'value'),
        Input('electrolyzer_type', 'value')
    ]
)
def update_graph(offshore_wind_lcoe, solar_lcoe, onshore_wind_lcoe, electrolyzer_type):
    global cap_factor_sources
    cap_factor_sources = capacity_factor(offshore_wind_lcoe, solar_lcoe, onshore_wind_lcoe)
    return global_lcoh(electrolyzer_type)

if __name__ == '__main__':
    app.run_server(debug=True)
