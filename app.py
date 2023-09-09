import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count

app = dash.Dash(__name__)

# Define custom color codes
background_color = '#f2f2f2'  # Light gray background
header_color = '#333333'  # Dark gray header
text_color = '#000000'  # Black text color

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
            figure=manufacturer_count(),
            style={'display': 'inline-block', 'width': '48%', 'margin-right': '2%'}
        ),  # Set the width to 48% and add some right margin
        dcc.Graph(
            figure=project_count(),
            style={'display': 'inline-block', 'width': '48%'}
        ),  # Set the width to 48%
    ], style={'text-align': 'center', 'margin-bottom': '10px'})
])

# Run the app if this script is the main module
if __name__ == '__main__':
    app.run_server(debug=False)
