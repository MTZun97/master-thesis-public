import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from manufacturer import manufacturer_count
from projects import project_count
from project_choropleth import generate_choropleth
from electrolyzer_cost_reduction import plot_cost_reduction
from global_lcoh import global_lcoh
from sensitivity import sensitivity_analysis
from country_timeline import create_timeline_plot
import plotly.graph_objects as go
from oxygen import create_O2revenue_plot
from carbontax import create_carbontax_plot

background_color = '#f2f2f2'
header_color = '#333333'
text_color = '#000000'
block_color = '#ffffff'


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(style={'background-color': background_color, 'padding': '20px'},
                      children=[
    html.Div([
        html.H1('Cost Projection of Global Green Hydrogen Production Scenarios',
                style={'font-size': '28px', 'color': header_color, 'margin-bottom': '5px'}),
        html.P([
            "Prepared by: ", html.B("Moe Thiri Zun, "),
            "Supervised by: ", html.B("Prof. Benjamin Craig McLellan, "),
            "Energy Economics Laboratory, Kyoto University"
        ], style={'font-size': '12px', 'color': text_color}),
    ], style={'text-align': 'center', 'margin-bottom': '10px'}),

    html.Hr(),
    html.Div([html.P([html.B("1. Country-wise Hydrogen Industry Landscape: Manfucturers, Projects, and Status Heatmap")],
                     style={'font-size': '18px', 'color': text_color})],
             style={
        'margin-bottom': '10px',
        'margin-left': '30px'
    }),


    html.Div([
        html.Div([
            html.P([
                "The analysis identifies 26 manufacturers of PEM electrolyzers, 24 manufacturers of alkaline electrolyzers, and only 4 manufacturers of SOEC technology. This observation suggests that SOEC electrolyzers for hydrogen production have not yet reached the commercial development stage, indicating ongoing research and development efforts in this area. In addition, an examination of the geographical distribution of manufacturing companies reveals that the majority of these companies are located in Germany and the United States, indicating that the electrolyzer industry is currently centered in the western part of the world. The concentration in the Western nations suggests that these regions are at the forefront of electrolyzer research and development, indicating their leadership in advancing the electrolyzer industry."
            ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='manufacturer-count',
                  figure=manufacturer_count(),
                  style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),
    

    html.Div([
        html.Div([
            html.P([
                "Considering the project statuses, approximately 97.8% of the identified projects are still in the early phases of development, which include the concept and feasibility study phases. Only 0.07% of projects have reached the operational stage, demonstrating the small number of hydrogen initiatives that have reached the commercialization stage. In addition, 2.1% of projects have reached the stage of Financial Investment Decision (FID) and are under construction, indicating the financial commitment to these ventures. Lastly, the rest of the initiatives are successful demonstrations of technologies related to hydrogen.",
                html.Br(), html.Br(), "Data Source: IEA Hydrogen Projects Database"
            ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='project-count',
                  figure=project_count(),
                  style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),

    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),

    html.Div([
        html.Div([
            html.Label('Select Status of Projects:', style={
                'font-weight': 'bold', 'margin-bottom': '10px', 'text-align': 'left', 'font-size': '16px'}),
            dcc.Dropdown(
                id='status-dropdown',
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Concept', 'value': 'Concept'},
                    {'label': 'Financial Investment Decision', 'value': 'FID'},
                    {'label': 'Feasibility Study', 'value': 'Feasibility study'},
                    {'label': 'Operational', 'value': 'Operational'},
                    {'label': 'DEMO', 'value': 'DEMO'},
                    {'label': 'Under construction', 'value': 'Under construction'},
                    {'label': 'Decommissioned', 'value': 'Decommissioned'}
                ],
                value='all',
                style={'width': '100%', 'margin-bottom': '15px',
                       'border-radius': '4px'}
            ),
            html.P([
                "Considering the project statuses, approximately 97.8% of the identified projects are still in the early phases of development, which include the concept and feasibility study phases. Only 0.07% of projects have reached the operational stage, demonstrating the small number of hydrogen initiatives that have reached the commercialization stage. In addition, 2.1% of projects have reached the stage of Financial Investment Decision (FID) and are under construction, indicating the financial commitment to these ventures. Lastly, the rest of the initiatives are successful demonstrations of technologies related to hydrogen.",
                html.Br(), html.Br(), "Data Source: IEA Hydrogen Projects Database"
            ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '78vh',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='choropleth', style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '80vh',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),

    html.Hr(),
    html.Div([html.P([html.B("2. Cost Reduction Potential of Electrolyzer Technologies: Single and Double Curve Fitting")],
                     style={'font-size': '18px', 'color': text_color})],
             style={
        'margin-bottom': '10px',
        'margin-left': '30px'
    }),

    html.Div([
        html.Div([
            html.Label('Select Methodology of Electrolyzer Cost Reduction:', style={
                'font-weight': 'bold', 'margin-bottom': '10px', 'text-align': 'left', 'font-size': '16px'}),
            dcc.Dropdown(
                id='method-dropdown',
                options=[
                    {'label': 'Single Curve Fitting', 'value': 'Single'},
                    {'label': 'Double Curve Fitting', 'value': 'Double'}
                ],
                value='Single',
                style={'width': '100%', 'margin-bottom': '15px',
                       'border-radius': '4px'},
            ),
            html.P([
                html.Table([
                    html.Tr([html.Th("Parameter", style={'padding': '0 10px'}), html.Th(
                        "Alkaline", style={'padding': '0 10px'}), html.Th("PEM", style={'padding': '0 10px'})]),
                    html.Tr([html.Td("Single Curve Fitting Decline Rate", style={'padding': '0 10px'}), html.Td(
                        "4.4%", style={'padding': '0 10px'}), html.Td("3.4%", style={'padding': '0 10px'})]),
                    html.Tr([html.Td("Double Curve Fitting Decline Rate", style={'padding': '0 10px'}), html.Td(
                        "3%", style={'padding': '0 10px'}), html.Td("4.3%", style={'padding': '0 10px'})]),
                    html.Tr([html.Td("Scaling Effect", style={'padding': '0 10px'}), html.Td(
                        "0.37", style={'padding': '0 10px'}), html.Td("0.6", style={'padding': '0 10px'})]),
                    html.Tr([html.Td("Learning Rate", style={'padding': '0 10px'}), html.Td(
                        "8%", style={'padding': '0 10px'}), html.Td("10%", style={'padding': '0 10px'})]),
                ]),
                html.Br(), html.Br(),
                "By 2050, Alkaline electrolyzers could potentially reduce costs by 77% and PEM electrolyzers by 79%, factoring in scaling and technological learning. These cost reductions depend on incline rates of system size and installed capacity. In the scaling scenario, the alkaline electrolyzer  has a 6% incline rate to 70 MW, while PEM electrolyzers assumed 3% to 15 MW. For technological learning, a 10% incline rate led Alkaline electrolyzers to 7 GW and 20% for PEM electrolyzers to 70 GW."
            ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='cost-reduction-plot', style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),

    html.Hr(),
    html.Div([html.P([html.B("3. Global Outlook for Green Hydrogen Production Cost")],
                     style={'font-size': '18px', 'color': text_color})],
             style={
        'margin-bottom': '10px',
        'margin-left': '30px'
    }),


    html.Div([
        html.Div([
            html.Div([
                html.Label("Electrolyzer Type:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                dcc.Dropdown(
                    id='electrolyzer_type',
                    options=[
                        {'label': 'Alkaline', 'value': 'alk'},
                        {'label': 'PEM', 'value': 'pem'}
                    ],
                    value='alk',
                    style={'width': '100%'}
                ),
            ], style={'margin-bottom': '20px'}),

            html.P([
                "Both electrolyzers demonstrate that onshore wind-based LCOH is cost-competitive, with potential for solar-based LCOH to drop below $1/kg H2. This suggests that substantial electrolyzer cost reductions could lead to a convergence of solar and onshore wind LCOH, enhancing the hydrogen production prospects of these renewable sources and encouraging broader green hydrogen adoption. This could facilitate a shift towards a hydrogen economy. Despite technological advancements, offshore wind-based LCOH remains the least cost-effective renewable option throughout the analysis, possibly owing to elevated installation, maintenance costs, or specific offshore challenges.",
            ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '380px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='lcoh_graph', style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '400px',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),


    html.Div([
        html.Div([
            html.Label('Percent change for sensitivity analysis', style={
                       'display': 'inline-block', 'width': '250px'}),
            dcc.Input(id='percent_change', type='number', value=0.3,
                      min=0.1, max=0.95, step=0.05,  style={'width': '100px'}),
            html.Br(),
            html.Br(),
            html.Span("Define values for base scenario:", style={
                      'font-weight': 'bold', 'margin-bottom': '10px'}),
            html.Br(),
            html.Div([
                html.Label('Startup year', style={
                           'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='startup_year', type='number', value=2020,
                          min=1992, max=2050, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Capacity factor (%)', style={
                           'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='cap_factor', type='number', value=50,
                          min=10, max=95, step=5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Current Density (A/cm²)',
                           style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='current_density', type='number', value=1.5,
                          min=0.2, max=2, step=0.05, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Electrolyzer Cost ($/kW)',
                           style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_cost', type='number',
                          value=1000, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Electrolyzer Efficiency (%)', style={
                           'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_efficiency', type='number',
                          value=50, min=1, max=99, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Water Rate ($/gal)',
                           style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='water_rate', type='number',
                          value=0.002, step = 0.001, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),
            html.Div([
                html.Label('Electricity Price ($/MWh)',
                           style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='elect_price', type='number',
                          value=36, step = 1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.P([
                    "Increasing efficiency and optimizing capacity factors emerge as key areas to focus on for reducing LCOH, with asymmetries in these relationships underscoring the need to prioritize efforts that prevent decreases. As an example, at low capacity factors, electrolyzer costs intensify despite similar changes, emphasizing the need for optimization while considering maintenance and equipment lifespan."
                ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
            ], style={'margin-bottom': '10px'}),

        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),


        dcc.Graph(id='tornado_chart', style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),
        ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),


    html.Div([
        html.Div([
            html.Div([
                html.Span(
                    "Enter the target LCOH:",
                    style={
                        'font-weight': 'bold',
                        "display": 'inline-block',
                        'margin-right': '10px',
                        'font-size': '16px'
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
                        'display': 'inline-block',
                        'border-radius': '4px',
                    }
                )
            ], style={
                'margin-bottom': '10px'
            }),
            html.Div([
                html.P([
                    html.Table([
                        html.Tr([html.Th("Scenarios", style={'padding': '0 20px'}), html.Th(
                            "LCOE", style={'padding': '0 5px'}), html.Th("Electrolzyer", style={'padding': '0 10px'})]),
                        html.Tr([html.Td("Optimistic", style={'padding': '0 20px'}), html.Td(
                            "Percent Decline", style={'padding': '0 5px'}), html.Td("R&D + Scaling + Learning Based Decline", style={'padding': '0 10px'})]),
                        html.Tr([html.Td("Pessimistic", style={'padding': '0 20px'}), html.Td(
                            "Stable", style={'padding': '0 5px'}), html.Td("R&D Based Decline", style={'padding': '0 10px'})]),
                    ], style = {'font-size':'12px'}),
                html.Br(),                    
                    "This analysis has significant implications for global energy and hydrogen markets. Early achievers like Spain and China may become green hydrogen exporters, while latecomers like Japan and South Korea could be key importers. This trajectory aligns with individual country roadmaps and is shaped by factors like renewable energy deployment pace, electrolyzer advancements, and policy support for the green hydrogen sector, shaping the evolving global market. However, the study prioritizes solar and onshore wind energy due to their widespread adoption, potentially missing cost-effective options like nuclear power in France, which warrants further analysis."
                ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',})
            ]),
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '58vh',
                       'background-color': '#f9f9f9', 'padding':'10px'}),


        dcc.Graph(
            id='timeline_graph',
            style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '60vh',}
        )
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),

    html.Hr(),
    html.Div([html.P([html.B("4. Revenue Beyond Hydrogen")],
                     style={'font-size': '18px', 'color': text_color})],
             style={
        'margin-bottom': '10px',
        'margin-left': '30px'
    }),


    html.Div([
        html.Div([
            html.Div([
                html.Span("Define values for Additional Capital Cost:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                html.Label('ASU Cost ($/tonO2)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='ASU_cost', type='number', value=200, min=0, step=5, style={'width': '100px'}),
                html.Br(),
                html.Br(),
                html.Span("Define values for base scenario:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                html.Br(),
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electricity Price ($/MWh)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electricity_price_O2', type='number', value=36, min=0, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electrolyzer Efficiency (%)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_efficiency_O2', type='number', value=70, min=0, max=100, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electrolyzer Cost ($/kW)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_cost_O2', type='number', value=1000, min=0, step=5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Capacity Factor (%)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='capacity_factor_O2', type='number', value=60, min=0, max=99, step=5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Natural Gas Price ($/MWh)', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='NG_price', type='number', value=10, min=0, step=1, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.P([
                    "Examining the impact of an oxygen revenue stream on the levelized cost of hydrogen reveals potential financial benefits. Under a 50% capacity factor and a $50/MWh electricity price, an additional capital cost of $200/tonO2 for an air separation unit is factored in. To compete with the LCOH without oxygen revenue, a minimum retail price of $2.1/kgO2 is essential. Moreover, to be competitive with grey hydrogen (priced at 30 €/MWh), a retail price of $3.1/kgO2 or higher is necessary. The identified oxygen selling price, approximately $3/kgO2, is on the lower end for high-purity oxygen, indicating that favorable market conditions could make electrolysis a cost-effective method for hydrogen production."
                ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
            ], style={'margin-bottom': '10px'}),
            
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='oxygen_plot', 
                style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),


    html.Div([
        html.Div([
            html.Span("Carbon Tax Plot Parameters:", style={'font-weight': 'bold'}),
            html.Br(),
            html.Br(),

            html.Div([
                html.Label('Natural Gas Price ($/MWh):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='NG_price_CO2', type='number', value=30, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Additional Cost of CCUS (%):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='CCUS_percent', type='number', value=30, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Capture Rate (%):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='capture_rate', type='number', value=90, min = 0, max = 100, step = 5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Carbon Tax ($/tonCO2):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='carbon_tax', type='number', value=100, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electricity Price Start ($/kWh):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electricity_price_CO2_start', type='number', value=0.01, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electricity Price End ($/kWh):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electricity_price_CO2_end', type='number', value=0.11, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electrolyzer Efficiency (%):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_efficiency_CO2', type='number', value=70, min = 0, max = 95, step = 5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Electrolyzer Cost ($/kW):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='electrolyzer_cost_CO2', type='number', value=1000, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.Label('Capacity Factor (%):', style={'display': 'inline-block', 'width': '250px'}),
                dcc.Input(id='capacity_factor_CO2', type='number', value=60, min = 0, max = 95, step = 5, style={'width': '100px'})
            ], style={'margin-bottom': '10px'}),

            html.Div([
                html.P([
                    "Hydrogen production's economic feasibility hinges greatly on electricity costs and carbon taxes. Currently, to rival grey hydrogen (roughly $20/MWh), green hydrogen necessitates electricity prices below $22/MWh, considering current electrolyzer expenses. In the short to medium term, SMR with CCS/CCUS seems to be the most budget-friendly production route, with or without carbon taxation."
                ], style={'font-size': '14px', 'color': text_color, 'text-align': "justify", 'padding': '10px',
                       'border-radius': '4px',}),
            ], style={'margin-bottom': '10px'}),
            
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '10px',
                   'border-radius': '5px', "margin-left": "10px", 'height': '480px',
                       'background-color': '#f9f9f9', 'padding':'10px'}),

        dcc.Graph(id='carbon_tax_plot', style={'width': '70%', 'display': 'inline-block', 'margin-left': '15px',
                          'vertical-align': 'top','height': '500px',}),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'border-radius': '5px'}),

    html.Hr()
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
        Input('electrolyzer_type', 'value')
    ]
)
def update_graph(electrolyzer_type):
    return global_lcoh(electrolyzer_type)


@app.callback(
    Output('tornado_chart', 'figure'),
    [
        Input('percent_change', 'value'),
        Input('startup_year', 'value'),
        Input('cap_factor', 'value'),
        Input('current_density', 'value'),
        Input('electrolyzer_cost', 'value'),
        Input('electrolyzer_efficiency', 'value'),
        Input('water_rate', 'value'),
        Input('elect_price', 'value')
    ]
)
def update_tornado_chart(percent_change, startup_year, cap_factor, current_density, electrolzyer_cost, electrolyzer_efficiency, water_rate, elect_price):
    return sensitivity_analysis(
        percent_change=percent_change,
        startup_year=startup_year,
        cap_factor=cap_factor/100,
        current_density=current_density,
        electrolzyer_cost=electrolzyer_cost,
        electrolyzer_efficiency=electrolyzer_efficiency,
        water_rate=water_rate,
        elect_price=elect_price/1000
    )



@app.callback(
    Output('timeline_graph', 'figure'),
    [Input('cost_target_input', 'value')]
)
def update_output(cost_target):

    if cost_target is not None:
        return create_timeline_plot(cost_target)
    else:
        return go.Figure()  

@app.callback(
    Output('oxygen_plot', 'figure'),
    [
        Input('ASU_cost', 'value'),
        Input('electricity_price_O2', 'value'),
        Input('electrolyzer_efficiency_O2', 'value'),
        Input('electrolyzer_cost_O2', 'value'),
        Input('capacity_factor_O2', 'value'),
        Input('NG_price', 'value')
    ]
)
def update_plot(ASU_cost, electricity_price_O2, electrolyzer_efficiency_O2, electrolyzer_cost_O2, capacity_factor_O2, NG_price):
    return create_O2revenue_plot(ASU_cost, electricity_price_O2/1000, electrolyzer_efficiency_O2, electrolyzer_cost_O2, capacity_factor_O2, NG_price)


@app.callback(
    Output('carbon_tax_plot', 'figure'),
    [
        Input('NG_price_CO2', 'value'),
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
def update_graph(NG_price_CO2, CCUS_percent, capture_rate, carbon_tax, electricity_price_CO2_start,
                 electricity_price_CO2_end, electrolyzer_efficiency_CO2, electrolyzer_cost_CO2,
                 capacity_factor_CO2):

    return create_carbontax_plot(NG_price_CO2, CCUS_percent, capture_rate, carbon_tax,
        [electricity_price_CO2_start, electricity_price_CO2_end],
        electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, capacity_factor_CO2/100
    )

if __name__ == '__main__':
    app.run_server(debug=False)
