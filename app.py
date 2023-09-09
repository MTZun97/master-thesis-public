import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div([
        html.H1('Cost Projection of Global Green Hydrogen Production Scenarios', style={'font-size': 22}),
        html.Span(children=[
            "Prepared by: ", html.B("Moe Thiri Zun"), html.Br(),
            "Energy Economics Laboratory, Kyoto University"
        ], style={'font-size': 16, 'color': '#000000'}),
        html.Br(),
        html.Br(),
        # Dropdown for selecting the figure
        dcc.Dropdown(
            id='figure-dropdown',
            options=[
                {'label': 'Manufacturer Count', 'value': 'manufacturer'},
                {'label': 'Project Count', 'value': 'project'},
            ],
            value='manufacturer',  # Default selection
            style={
                'width': '50%',  # Set the width of the dropdown
                'font-size': '16px',  # Adjust the font size
                'color': '#333',  # Text color
                'background-color': '#fff',  # Background color
                'border': '2px solid #007BFF',  # Border style
                'border-radius': '5px',  # Border radius
                'padding': '10px',  # Padding
                'box-shadow': '0px 2px 4px rgba(0, 0, 0, 0.2)',  # Add a box shadow
            }
        ),

        # Placeholder for the selected figure
        dcc.Graph(id='selected-figure', style={'width': '90%', 'height': '100vh'}),  # Set width and height to 100%
    ], style={'text-align': 'center'}),
])


@app.callback(
    Output('selected-figure', 'figure'),
    Input('figure-dropdown', 'value')
)
def update_selected_figure(selected_value):
    if selected_value == 'manufacturer':
        return manufacturer_count()
    elif selected_value == 'project':
        return project_count()
    else:
        # Handle an invalid selection (optional)
        return None


if __name__ == '__main__':
    app.run_server(debug=False)
