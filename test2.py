import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count
from project_choropleth import generate_choropleth
from electrolyzer_cost_reduction import plot_cost_reduction  # Corrected missing import statement
from global_lcoh import capacity_factor, global_lcoh


# Define custom color codes
background_color = '#f2f2f2'  # Light gray background
header_color = '#333333'  # Dark gray header
text_color = '#000000'  # Black text color
block_color = '#ffffff'  # White block background color

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of your app
app.layout = html.Div(style={'background-color': background_color, 'padding': '20px'}, children=[
    html.Div([
        html.H1('Cost Projection of Global Green Hydrogen Production Scenarios',
                style={'font-size': '28px', 'color': header_color, 'margin-bottom': '10px'}),
        html.P([
            "Prepared by: ", html.B("Moe Thiri Zun"), html.Br(),
            "Energy Economics Laboratory, Kyoto University"
        ], style={'font-size': '16px', 'color': text_color}),
    ], style={'text-align': 'center', 'margin-bottom': '10px'}),
    
    html.Div([
        dcc.Graph(
            id='manufacturer-count',
            figure=manufacturer_count(),
            style={'display': 'inline-block', 'width': '48%', 'margin-right': '2%'}
        ),
        dcc.Graph(
            id='project-count',
            figure=project_count(),
            style={'display': 'inline-block', 'width': '48%'}
        ),
    ], style={'text-align': 'center', 'margin-bottom': '10px'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Label('Select Status:', style={'font-weight': 'bold', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id='status-dropdown',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Concept', 'value': 'Concept'},
                {'label': 'FID', 'value': 'FID'},
                {'label': 'Feasibility Study', 'value': 'Feasibility study'},
                {'label': 'Operational', 'value': 'Operational'},
                {'label': 'DEMO', 'value': 'DEMO'},
                {'label': 'Under construction', 'value': 'Under construction'},
                {'label': 'Decommissioned', 'value': 'Decommissioned'}  # Corrected typo in 'Decommissioned'
            ],
            value='all',
            style={'width': '100%'}
        )
    ], style={'width': '50%', 'margin': '0 auto', 'margin-bottom': '20px'}),
    
    dcc.Graph(id='choropleth', style={'width': '100%', 'height': '80vh', 'margin': '0 auto'}),
    
    html.Br(),
    html.Br(),
    
    html.Div([
        html.Label('Select Methodology:', style={'font-weight': 'bold', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id='method-dropdown',
            options=[
                {'label': 'Single Curve Fitting', 'value': 'Single'},
                {'label': 'Double Curve Fitting', 'value': 'Double'}
            ],
            value='Single',
            style={'width': '100%'}
        )], style={'width': '50%', 'margin': '0 auto', 'margin-bottom': '20px'}),
    dcc.Graph(id='cost-reduction-plot', style={'width': '100%', 'height': '80vh', 'margin': '0 auto'}),
    html.Br(),
    html.Br(),
    html.Div([
    html.Span("Enter the capacity factors for each source:", style={'font-weight': 'bold', "display": 'block', 'text-align': 'center', 'margin-bottom': '10px'}),
    html.Div([
        html.Label("Offshore Wind LCOE:", style={'margin-right': '10px','margin-left': '10px'}),
        dcc.Input(id='offshore_wind_lcoe', type='number', value=0.23, step=0.01, min=0.1, max=1),
        html.Label("Solar LCOE:", style={'margin-right': '10px','margin-left': '10px'}),
        dcc.Input(id='solar_lcoe', type='number', value=0.12, step=0.1, min=0.01, max=1),
        html.Label("Onshore Wind LCOE:", style={'margin-right': '10px','margin-left': '10px'}),
        dcc.Input(id='onshore_wind_lcoe', type='number', value=0.23, step=0.01, min=0.1, max=1),
    ], style={'width': '50%', 'margin': '0 auto', 'margin-bottom': '10px', "display": 'block', "text-align": 'center'}),
    html.Br(),

    html.Div([
        html.Label("Electrolyzer Type:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id='electrolyzer_type',
            options=[
                {'label': 'Alkaline', 'value': 'alk'},
                {'label': 'PEM', 'value': 'pem'}
            ],
            value='alk', style={'width': '100%'}
        ),
    ], style={'width': '50%', 'margin': '0 auto', 'margin-bottom': '20px'}),
    dcc.Graph(id='lcoh_graph')])

])

@app.callback(
    Output('choropleth', 'figure'),
    Input('status-dropdown', 'value')
)
def update_choropleth(status):
    choropleth_fig = generate_choropleth(status)
    return choropleth_fig

@app.callback(
    Output('cost-reduction-plot', 'figure'),
    Input('method-dropdown', 'value')
)
def update_cost_reduction_plot(selected_method):
    return plot_cost_reduction(selected_method)

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

# Run the app if this script is the main module
if __name__ == '__main__':
    app.run_server(debug=True)
