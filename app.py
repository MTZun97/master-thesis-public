import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count
from project_choropleth import generate_choropleth
from electrolyzer_cost_reduction import plot_cost_reduction  
from global_lcoh import capacity_factor, global_lcoh
from sensitivity import sensitivity_analysis
from country_timeline import create_timeline_plot
import plotly.graph_objects as go
from oxygen import create_O2revenue_plot

background_color = '#f2f2f2'  
header_color = '#333333'  
text_color = '#000000'  
block_color = '#ffffff' 


app = dash.Dash(__name__)
server = app.server


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
                {'label': 'Decommissioned', 'value': 'Decommissioned'}  
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
        html.Label("Offshore Wind:", style={'margin-right': '10px','margin-left': '10px'}),
        dcc.Input(id='offshore_wind_lcoe', type='number', value=0.23, step=0.01, min=0.1, max=1),
        html.Label("Solar:", style={'margin-right': '10px','margin-left': '10px'}),
        dcc.Input(id='solar_lcoe', type='number', value=0.12, step=0.01, min=0.1, max=1),
        html.Label("Onshore Wind:", style={'margin-right': '10px','margin-left': '10px'}),
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
    dcc.Graph(id='lcoh_graph')]),

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
            dcc.Input(id='electrolyzer_efficiency', type='number', value=50, min=1, max=99, step=0.1, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),        
        
        html.Div([
            html.Label('Water Rate ($/gal)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='water_rate', type='number', value=0.002, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
        
        html.Div([
            html.Label('Electricity Price ($/kWh)', style={'display': 'inline-block', 'width': '300px'}), 
            dcc.Input(id='elect_price', type='number', value=0.036, style={'width': '100px'})
        ], style={'margin-bottom': '10px'}),
    ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top', 'padding': '5px', 'margin': '10px', 'background-color': block_color}),
    
    dcc.Graph(id='tornado_chart', style={'display': 'inline-block', 'width': '65%', 'vertical-align': 'top',  'padding': '5px', 'margin': '10px', 'background-color': block_color }),

    html.Div([
    html.Div([
        html.Span(
            "Enter the target LCOH:", 
            style={
                'font-weight': 'bold', 
                "display": 'inline-block', 
                'margin-right': '10px',  # Added some margin to separate the text and input box
                'vertical-align': 'middle'  # Align the text vertically with the input box
            }
        ),
        dcc.Input(
            id='cost_target_input', 
            value=2, 
            type='number', 
            min=0, 
            max=5, 
            step=0.5, 
            style={
                'width': '100px', 
                'display': 'inline-block',  # Changed display to inline-block
                'vertical-align': 'middle'  # Align the input box vertically with the text
            }
        )], 
        style={
            "width": "100%", 
            'text-align': 'center', 
        }
    ),
    
    # Graph to display the output
    dcc.Graph(
        id='output_graph', 
        figure=create_timeline_plot(2), 
        style={
            'width': '100%', 
            'vertical-align': 'top',  
            'padding': '5px', 
            'margin': '10px', 
            'background-color': block_color
        }
    )
]),
    html.Div([
        html.Div([          
            html.Div([
                html.Label('ASU Cost', style={'display': 'inline-block', 'width': '300px'}),
                dcc.Input(id='ASU_cost', type='number', value=200, min=0, step=5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            
            html.Div([
                html.Label('Electricity Price', style={'display': 'inline-block', 'width': '300px'}),
                dcc.Input(id='electricity_price_O2', type='number', value=0.036, min=0.01, step=0.001, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            
            html.Div([
                html.Label('Electrolyzer Efficiency', style={'display': 'inline-block', 'width': '300px'}),
                dcc.Input(id='electrolyzer_efficiency_O2', type='number', value=70, min=0, max=100, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            
            html.Div([
                html.Label('Electrolyzer Cost', style={'display': 'inline-block', 'width': '300px'}),
                dcc.Input(id='electrolyzer_cost_O2', type='number', value=1000, min=0, step=5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            
            html.Div([
                html.Label('Capacity Factor', style={'display': 'inline-block', 'width': '300px'}),
                dcc.Input(id='capacity_factor_O2', type='number', value=0.6, min=0, max=1, step=0.01, style={'width': '100px'})
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
        ], style={'display': 'inline-block', 'width': '30%', 'vertical-align': 'top', 'padding': '5px', 'margin': '10px', 'background-color': block_color}),
        
        dcc.Graph(id='line_plot', style={'display': 'inline-block', 'width': '65%', 'vertical-align': 'top',  'padding': '5px', 'margin': '10px', 'background-color': block_color }),
    ])
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


# Define the callback to update the graph
@app.callback(
    Output('output_graph', 'figure'),
    [Input('cost_target_input', 'value')]
)
def update_output(cost_target):
    # Call your function to generate the plot
    if cost_target is not None:
        return create_timeline_plot(cost_target)
    else:
        return go.Figure()  # This will be an empty figure

@app.callback(
    Output('line_plot', 'figure'),
    [
        Input('ASU_cost', 'value'),
        Input('electricity_price_O2', 'value'),
        Input('electrolyzer_efficiency_O2', 'value'),
        Input('electrolyzer_cost_O2', 'value'),
        Input('capacity_factor_O2', 'value'),
        Input('NG_price', 'value'),
        Input('O2_price_slider', 'value')
    ]
)
def update_plot(ASU_cost, electricity_price_O2, electrolyzer_efficiency_O2, electrolyzer_cost_O2, capacity_factor_O2, NG_price, O2_price):
    return create_O2revenue_plot(ASU_cost, electricity_price_O2, electrolyzer_efficiency_O2, electrolyzer_cost_O2, capacity_factor_O2, NG_price, O2_price)


if __name__ == '__main__':
    app.run_server(debug=True)
