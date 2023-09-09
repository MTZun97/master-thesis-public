import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count
from project_choropleth import generate_choropleth

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
        ),  # Set the width to 48% and add some right margin
        dcc.Graph(
            id='project-count',
            figure=project_count(),
            style={'display': 'inline-block', 'width': '48%'}
        ),  # Set the width to 48%
    ], style={'text-align': 'center', 'margin-bottom': '10px'}),
    
    html.Br(),
    html.Br(),
    html.Div([
        html.Label('Select Status:', style={'font-weight': 'bold'}),
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
                {'label': 'Decommisioned', 'value': 'Decommisioned'}
            ],
            value='all',
            style={'width': '100%'}  # Set the width of the dropdown
        )
    ], style={'width': '50%', 'margin': '0 auto', 'margin-bottom': '20px'}),
    
    dcc.Graph(id='choropleth', style={'width': '100%', 'height': '80vh', 'margin': '0 auto'})


])

@app.callback(
    Output('choropleth', 'figure'),
    Input('status-dropdown', 'value')
)
def update_choropleth(status):
    choropleth_fig = generate_choropleth(status)
    return choropleth_fig

# Run the app if this script is the main module
if __name__ == '__main__':
    app.run_server(debug=False)
