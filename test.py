from dash import Dash, Input, Output, html, dcc
from sensitivity import sensitivity_analysis

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Percent change for sensitivity analysis', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='percent_change', type='number', value=0.3, min=0.01, max=0.99, step=0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        html.Br(),
        html.Span("Define values for base scneario:", style={'font-weight': 'bold','margin-bottom': '300px'}),
        html.Br(),
        html.Div([
            html.Label('Startup year', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='startup_year', type='number', value=2020, min=1994, max= 2050, step=1, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Capacity factor', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='cap_factor', type='number', value=0.5, min=0.01, max=0.99, step= 0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Current Density (A/cm²)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='current_density', type='number', value=1.5,  min=0.2, max=2, step=0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electrolyzer Cost ($/kW)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electrolzyer_cost', type='number', value=1000, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electrolyzer Efficiency (%)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='electrolyzer_efficiency', type='number', value=50, min=0.01, max=0.99, step=0.01, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),        
        
        html.Div([
            html.Label('Water Rate', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='water_rate', type='number', value=0.00237495008, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electricity Price ($/kWh)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='elect_price', type='number', value=0.036, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
    ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top', 'border': '1px solid #ccc', 'padding': '10px', 'margin': '10px'}),
    
    dcc.Graph(id='tornado_chart', style={'display': 'inline-block', 'width': '65%', 'vertical-align': 'top', 'border': '1px solid #ccc', 'padding': '10px', 'margin': '10px'})
])

@app.callback(
    Output('tornado_chart', 'figure'),
    [
        Input('percent_change', 'value'),
        Input('startup_year', 'value'),
        Input('cap_factor', 'value'),
        Input('current_density', 'value'),
        Input('electrolzyer_cost', 'value'),
        Input('electrolyzer_efficiency', 'value'),
        Input('water_rate', 'value'),
        Input('elect_price', 'value')
    ]
)
def update_tornado_chart(percent_change, startup_year, cap_factor, current_density, electrolzyer_cost, electrolyzer_efficiency, water_rate, elect_price):
    return sensitivity_analysis(
        percent_change=percent_change,
        startup_year=startup_year,
        cap_factor=cap_factor,
        current_density=current_density,
        electrolzyer_cost=electrolzyer_cost,
        electrolyzer_efficiency=electrolyzer_efficiency,
        water_rate=water_rate,
        elect_price=elect_price
    )

if __name__ == '__main__':
    app.run_server(debug=True)
