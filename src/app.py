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
import numpy as np

background_color = '#f2f2f2'
header_color = '#333333'
text_color = '#000000'
block_color = '#ffffff'


app = dash.Dash(__name__, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],)
server = app.server


app.layout = html.Div(style={'background-color': background_color, 'padding': '2vh'},
                      children=[
    html.Div([
        html.H1('Cost Projection of Global Green Hydrogen Production Scenarios',
                style={'font-size': '2vw', 'color': header_color, 'margin-bottom': '0.5vh'}),
        html.P([
            "Prepared by: ", html.B("Moe Thiri Zun, "),
            "Supervised by: ", html.B("Prof. Benjamin Craig McLellan, "),
            "Energy Economics Laboratory, Kyoto University"
        ], style={'font-size': '0.8vw', 'color': text_color}),
    ], style={'text-align': 'center', 'margin-bottom': '1vh'}),

    html.Hr(),
    html.Div([html.P([html.B("1. Country-wise Hydrogen Industry Landscape: Manfucturers, Projects, and Status Heatmap")],
                     style={'font-size': '1.5vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),
    html.Div([html.P([html.B("1.1.Electrolyzer manufacturer count per country")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([
        html.Div([
            html.P([
                "The analysis identifies 26 manufacturers of PEM electrolyzers, 24 manufacturers of alkaline electrolyzers, and only 4 manufacturers of SOEC technology. This observation suggests that SOEC electrolyzers for hydrogen production have not yet reached the commercial development stage, indicating ongoing research and development efforts in this area. In addition, an examination of the geographical distribution of manufacturing companies reveals that the majority of these companies are located in Germany and the United States, indicating that the electrolyzer industry is currently centered in the western part of the world. The concentration in the Western nations suggests that these regions are at the forefront of electrolyzer research and development, indicating their leadership in advancing the electrolyzer industry."
            ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                      'border-radius': '0.4vh', }),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='manufacturer-count',
                  figure=manufacturer_count(),
                  style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                         'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Div([html.P([html.B("1.2. Project count per country")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([
        html.Div([
            html.P([
                "Considering the project statuses, approximately 97.8% of the identified projects are still in the early phases of development, which include the concept and feasibility study phases. Only 0.07% of projects have reached the operational stage, demonstrating the small number of hydrogen initiatives that have reached the commercialization stage. In addition, 2.1% of projects have reached the stage of Financial Investment Decision (FID) and are under construction, indicating the financial commitment to these ventures. Lastly, the rest of the initiatives are successful demonstrations of technologies related to hydrogen.",
                html.Br(), html.Br(), "Data Source: IEA Hydrogen Projects Database"
            ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                      'border-radius': '1vh', }),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='project-count',
                  figure=project_count(),
                  style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                         'vertical-align': 'top', 'height': '70vh', }),

    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Div([html.P([html.B("1.3. Total current and projected installed capacity per country")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([
        html.Div([
            html.Label('Select Status of Projects:', style={
                'font-weight': 'bold', 'margin-bottom': '3vh', 'text-align': 'left', 'font-size': '0.9vw','margin-bottom': '2vh',}),
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
                style={'width': '100%', 'margin-bottom': '1.5vh',
                       'border-radius': '0.4vh', 'font-size': '1vw', 'text-align':'center'}
            ),
            html.P([
                "Considering the project statuses, approximately 97.8% of the identified projects are still in the early phases of development, which include the concept and feasibility study phases. Only 0.07% of projects have reached the operational stage, demonstrating the small number of hydrogen initiatives that have reached the commercialization stage. In addition, 2.1% of projects have reached the stage of Financial Investment Decision (FID) and are under construction, indicating the financial commitment to these ventures. Lastly, the rest of the initiatives are successful demonstrations of technologies related to hydrogen.",
                html.Br(), html.Br(), "Data Source: IEA Hydrogen Projects Database"
            ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                      'border-radius': '0.4vh', }),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '78vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='choropleth', style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                                          'vertical-align': 'top', 'height': '80vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '1.5vh'}),

    html.Hr(),
    html.Div([html.P([html.B("2. Cost Reduction Potential of Electrolyzer Technologies: Single and Double Curve Fitting")],
                     style={'font-size': '1.5vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([html.P([html.B("2.1. Cost reduction potential of alkaline and PEM electrolzyers")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([
        html.Div([
            html.Label('Select Methodology of Electrolyzer Cost Reduction:', style={
                'font-weight': 'bold', 'margin-bottom': '3vh', 'text-align': 'left', 'font-size': '0.9vw'}),
            dcc.Dropdown(
                id='method-dropdown',
                options=[
                    {'label': 'Single Curve Fitting', 'value': 'Single'},
                    {'label': 'Double Curve Fitting', 'value': 'Double'}
                ],
                value='Single',
                style={'width': '100%', 'margin-bottom': '1.5vh',
                       'border-radius': '0.4vh', 'font-size': '1vw', 'text-align':'center'},
            ),
            html.P([
                html.Table([
                    html.Tr([html.Th("Parameter", style={'padding': '0 1vh'}), html.Th(
                        "Alkaline", style={'padding': '0 1vh'}), html.Th("PEM", style={'padding': '0 1vh'})]),
                    html.Tr([html.Td("Single Curve Fitting Decline Rate", style={'padding': '0 1vh'}), html.Td(
                        "4.4%", style={'padding': '0 1vh'}), html.Td("3.4%", style={'padding': '0 1vh'})]),
                    html.Tr([html.Td("Double Curve Fitting Decline Rate", style={'padding': '0 1vh'}), html.Td(
                        "3%", style={'padding': '0 1vh'}), html.Td("4.3%", style={'padding': '0 1vh'})]),
                    html.Tr([html.Td("Scaling Effect", style={'padding': '0 1vh'}), html.Td(
                        "0.37", style={'padding': '0 1vh'}), html.Td("0.6", style={'padding': '0 1vh'})]),
                    html.Tr([html.Td("Learning Rate", style={'padding': '0 1vh'}), html.Td(
                        "8%", style={'padding': '0 1vh'}), html.Td("10%", style={'padding': '0 1vh'})]),
                ]),
                html.Br(), html.Br(),
                "By 2050, Alkaline electrolyzers could potentially reduce costs by 77% and PEM electrolyzers by 79%, factoring in scaling and technological learning. These cost reductions depend on incline rates of system size and installed capacity. In the scaling scenario, the alkaline electrolyzer  has a 6% incline rate to 70 MW, while PEM electrolyzers assumed 3% to 15 MW. For technological learning, a 10% incline rate led Alkaline electrolyzers to 7 GW and 20% for PEM electrolyzers to 70 GW."
            ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                      'border-radius': '0.4vh', }),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='cost-reduction-plot', style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                                                   'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Hr(),
    html.Div([html.P([html.B("3. Global Outlook for Green Hydrogen Production Cost")],
                     style={'font-size': '1.5vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([html.P([html.B("3.1. Global levelized cost of hydrogen (LCOH) for different renewable energy sources")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Label("Electrolyzer Type:", style={
                           'font-weight': 'bold', 'margin-bottom': '3vh', 'font-size': '0.9vw'}),
                dcc.Dropdown(
                    id='electrolyzer_type',
                    options=[
                        {'label': 'Alkaline', 'value': 'alk'},
                        {'label': 'PEM', 'value': 'pem'}
                    ],
                    value='alk',
                    style={'width': '100%', 'font-size': '1vw', 'text-align':'center'}
                ),
            ], style={'margin-bottom': '2vh'}),

            html.P([
                "Both electrolyzers demonstrate that onshore wind-based LCOH is cost-competitive, with potential for solar-based LCOH to drop below $1/kg H2. This suggests that substantial electrolyzer cost reductions could lead to a convergence of solar and onshore wind LCOH, enhancing the hydrogen production prospects of these renewable sources and encouraging broader green hydrogen adoption. This could facilitate a shift towards a hydrogen economy. Despite technological advancements, offshore wind-based LCOH remains the least cost-effective renewable option throughout the analysis, possibly owing to elevated installation, maintenance costs, or specific offshore challenges.",
            ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                      'border-radius': '0.4vh', }),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='lcoh_graph', style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                                          'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Div([html.P([html.B("3.2. Sensitivity analysis of green hydrogen production cost")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '1vh'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Label('Change for sensitivity analysis (%)', style={
                        'display': 'inline-block', 'width': '25%', "font-size": "0.9vw"}),
                html.Div([
                    dcc.Slider(
                        id='percent_change',
                        min=0,
                        max=100,
                        value=30,
                        marks={0:"0", 100:"100"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Br(),
            html.Span("Define values for base scenario:", style={
                      'font-weight': 'bold', 'margin-bottom': '1vh', "font-size": "0.9vw"}),
            html.Br(),
            html.Div([
                html.Label('Startup year', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='startup_year',
                        min=1992,
                        max=2050,
                        value=2020,
                        marks={1992: "1992", 2050: "2050"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1  # This makes the slider continuous
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label('Capacity factor (%)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='cap_factor',
                        min=0,
                        max=100,
                        value=50,
                        marks={0: "0", 100: "100"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),
            
            html.Div([
                html.Label('Current Density (A/cm²)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='current_density',
                        min=0.2,
                        max=2,
                        value=1.5,
                        marks={0.2: "0.2", 2: "2"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=0.01
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label('Electrolyzer Cost ($/kW)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='electrolyzer_cost',
                        min=0,
                        max=10000,
                        value=1000,
                        marks={0: "0", 10000: "10000"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label('Electrolyzer Efficiency (%)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='electrolyzer_efficiency',
                        min=0,
                        max=101,
                        value=50,
                        marks={0: "0", 101: "101"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label('Water Rate ($/gal)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='water_rate',
                        min=0.001,
                        max=0.01,
                        value=0.002,
                        marks={0.001: "0.001", 0.01: "0.01"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=0.001
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label('Electricity Price ($/MWh)', style={
                    'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}),
                html.Div([
                    dcc.Slider(
                        id='elect_price',
                        min=0,
                        max=100,
                        value=36,
                        marks={0: "0", 100: "100"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1,
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),


            html.Div([
                html.P([
                    "Increasing efficiency and optimizing capacity factors emerge as key areas to focus on for reducing LCOH, with asymmetries in these relationships underscoring the need to prioritize efforts that prevent decreases. As an example, at low capacity factors, electrolyzer costs intensify despite similar changes, emphasizing the need for optimization while considering maintenance and equipment lifespan."
                ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                          'border-radius': '0.4vh', }),
            ], style={'margin-bottom': '1vh'}),

        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),


        dcc.Graph(id='tornado_chart', style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                                             'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Div([html.P([html.B("3.3. Timeline plot of countries to achieve target LCOH")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '1vh'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Label(
                    "Enter the target LCOH ($/kg):",
                    style={
                        'font-weight': 'bold',
                        "display": 'inline-block',
                        'width': '25%',  # Adjusted width
                        'font-size': '0.9vw'
                    }
                ),
                html.Div([
                    dcc.Slider(
                        id='cost_target_input',
                        value=2,
                        min=0.1,
                        max=5,
                        marks={0.1: "0.1", 5: "5"},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=0.1,
                    )
                ], style={'width': '75%', 'display': 'inline-block'}),  # Adjusted width and display
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),
            html.Div([
                html.P([
                    html.Table([
                        html.Tr([html.Th("Scenarios", style={'padding': '0 2vh'}), html.Th(
                            "LCOE", style={'padding': '0 0.5vh'}), html.Th("Electrolzyer", style={'padding': '0 1vh'})]),
                        html.Tr([html.Td("Optimistic", style={'padding': '0 2vh'}), html.Td(
                            "Percent Decline", style={'padding': '0 0.5vh'}), html.Td("R&D + Scaling + Learning Based Decline", style={'padding': '0 1vh'})]),
                        html.Tr([html.Td("Pessimistic", style={'padding': '0 2vh'}), html.Td(
                            "Stable", style={'padding': '0 0.5vh'}), html.Td("R&D Based Decline", style={'padding': '0 1vh'})]),
                    ], style={'font-size': '0.9vw'}),
                    html.Br(),
                    "This analysis has significant implications for global energy and hydrogen markets. Early achievers like Spain and China may become green hydrogen exporters, while latecomers like Japan and South Korea could be key importers. This trajectory aligns with individual country roadmaps and is shaped by factors like renewable energy deployment pace, electrolyzer advancements, and policy support for the green hydrogen sector, shaping the evolving global market. However, the study prioritizes solar and onshore wind energy due to their widespread adoption, potentially missing cost-effective options like nuclear power in France, which warrants further analysis."
                ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                          'border-radius': '0.4vh', })
            ]),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),


        dcc.Graph(
            id='timeline_graph',
            style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                   'vertical-align': 'top', 'height': '70vh', }
        )
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Hr(),
    html.Div([html.P([html.B("4. Revenue Beyond Hydrogen")],
                     style={'font-size': '1.5vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '3vh'
    }),

    html.Div([html.P([html.B("4.1. Impact of additional oxygen revenue on LCOH")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '1vh'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Span("Define values for Additional Capital Cost:", style={
                          'font-weight': 'bold', 'margin-bottom': '1vh', "font-size": "0.9vw"}),
                html.Div([
                    html.Label(
                        'ASU Cost ($/tonO2)',
                        style={
                            'display': 'inline-block',
                            'width': '25%',  # Adjusted width according to your new standard
                            'font-size': '0.9vw'
                        }
                    ),
                    html.Div([
                        dcc.Slider(
                            id='ASU_cost',
                            value=200,  # Default value
                            min=0,  # Minimum value
                            max=1000,  # Maximum value, you might want to adjust this
                            marks={0: '0', 1000: '1000'},  # Marks, you might want to adjust these
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Step value
                        )
                    ], style={'width': '75%', 'display': 'inline-block'}),  # Adjusted width and display
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Br(),
                html.Br(),
                html.Span("Define values for base scenario:", style={
                          'font-weight': 'bold', 'margin-bottom': '1vh'}),
                html.Br(),
            ], style={'margin-bottom': '1vh', "font-size": "0.9vw"}),

            html.Div([
                html.Label(
                    'Electricity Price ($/MWh)',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='electricity_price_O2',
                        value=36,
                        min=0,
                        max=100,  # Adjust maximum value as needed
                        marks={0: '0', 100: '100'},  # Adjust marks as needed
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label(
                    'Electrolyzer Efficiency (%)',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='electrolyzer_efficiency_O2',
                        value=70,
                        min=0,
                        max=100,
                        marks={0: '0', 100: '100'},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label(
                    'Electrolyzer Cost ($/kW)',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='electrolyzer_cost_O2',
                        value=1000,
                        min=0,
                        max=10000,  # Adjust maximum value as needed
                        marks={0: '0', 10000: '10000'},  # Adjust marks as needed
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label(
                    'Capacity Factor (%)',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='capacity_factor_O2',
                        value=60,
                        min=0,
                        max=100,
                        marks={0: '0', 100: '100'},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.Label(
                    'Natural Gas Price ($/MWh)',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='NG_price',
                        value=10,
                        min=0,
                        max=100,  # Adjust maximum value as needed
                        marks={0: '0', 100: '100'}, 
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                html.P([
                    "Examining the impact of an oxygen revenue stream on the levelized cost of hydrogen reveals potential financial benefits. Under a 50% capacity factor and a $50/MWh electricity price, an additional capital cost of $200/tonO2 for an air separation unit is factored in. To compete with the LCOH without oxygen revenue, a minimum retail price of $2.1/kgO2 is essential. Moreover, to be competitive with grey hydrogen (priced at 30 €/MWh), a retail price of $3.1/kgO2 or higher is necessary. The identified oxygen selling price, approximately $3/kgO2, is on the lower end for high-purity oxygen, indicating that favorable market conditions could make electrolysis a cost-effective method for hydrogen production."
                ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                          'border-radius': '0.4vh', }),
            ], style={'margin-bottom': '1vh', "font-size": "0.9vw"}),

        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.5vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='oxygen_plot',
                  style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                         'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

    html.Div([html.P([html.B("4.2. LCOH comparison: green, grey and blue hydrogen")],
                     style={'font-size': '1.3vw', 'color': text_color})],
             style={
        'margin-bottom': '1vh',
        'margin-left': '1vh'
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Label(
                    'Natural Gas Price ($/MWh):',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='NG_price_CO2',
                        value=30,
                        min=0,
                        max=100,
                        marks={0: '0', 100: '100'},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                    html.Label(
                        'Additional Cost of CCUS (%):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='CCUS_percent',
                            value=30,
                            min=0,
                            max=100,
                            marks={0: '0', 100: '100'},
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),


            html.Div([
                html.Label(
                    'Capture Rate (%):',
                    style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                ),
                html.Div([
                    dcc.Slider(
                        id='capture_rate',
                        value=90,
                        min=0,
                        max=100,
                        marks={0: '0', 100: '100'},
                        updatemode='drag',
                        tooltip={'placement': 'top', 'always_visible': False},
                        step=1
                    )
                ], style={'width': '75%', 'display': 'inline-block'})
            ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

            html.Div([
                    html.Label(
                        'Carbon Tax ($/tonCO2):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='carbon_tax',
                            value=100,
                            min=0,
                            max=500,  # Set max value based on your needs
                            marks={0: '0', 500: '500'},
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Div([
                    html.Label(
                        'Electricity Price Start ($/kWh):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='electricity_price_CO2_start',
                            value=10,
                            min=0,
                            max=100,  # Set max value based on your needs
                            marks={0: '0', 100: '100'},
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Div([
                    html.Label(
                        'Electricity Price End ($/kWh):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='electricity_price_CO2_end',
                            value=100,
                            min=0,  # Set min value based on your needs
                            max=100,  # Set max value based on your needs
                            marks={0: '0', 100: '100'},
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Div([
                    html.Label(
                        'Electrolyzer Efficiency (%):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='electrolyzer_efficiency_CO2',
                            value=70,
                            min=0,
                            max=100,  # Adjust max value as needed
                            marks={0: '0', 100: '100'},  # Adjust marks as needed
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Div([
                    html.Label(
                        'Electrolyzer Cost ($/kW):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='electrolyzer_cost_CO2',
                            value=1000,
                            min=0,
                            max=10000,  # Adjust max value as needed
                            marks={0: '0', 10000: '10000'},  # Adjust marks as needed
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=50  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),

                html.Div([
                    html.Label(
                        'Capacity Factor (%):',
                        style={'display': 'inline-block', 'width': '25%', 'font-size': '0.9vw'}
                    ),
                    html.Div([
                        dcc.Slider(
                            id='capacity_factor_CO2',
                            value=60,
                            min=0,
                            max=100,  # Adjust max value as needed
                            marks={0: '0', 100: '100'},  # Adjust marks as needed
                            updatemode='drag',
                            tooltip={'placement': 'top', 'always_visible': False},
                            step=1  # Set step based on your needs
                        )
                    ], style={'width': '75%', 'display': 'inline-block'})
                ], style={'margin-bottom': '1vh', 'display': 'flex', 'align-items': 'center'}),
            
            html.Div([
                html.P([
                    "Hydrogen production's economic feasibility hinges greatly on electricity costs and carbon taxes. Currently, to rival grey hydrogen, green hydrogen necessitates electricity prices below $22/MWh, considering current electrolyzer expenses. In the short to medium term, SMR with CCS/CCUS seems to be the most cost-effective route, with or without carbon taxation."
                ], style={'font-size': '0.9vw', 'color': text_color, 'text-align': "justify", 'padding': '1vh',
                          'border-radius': '0.4vh', }),
            ], style={'margin-bottom': '1vh'}),

        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '1vh',
                  'border-radius': '0.4vh', "margin-left": "1vh", 'height': '68vh',
                  'background-color': '#f9f9f9', 'padding': '1vh'}),

        dcc.Graph(id='carbon_tax_plot', style={'width': '65%', 'display': 'inline-block', 'margin-left': '1.5vh',
                                               'vertical-align': 'top', 'height': '70vh', }),
    ], style={'width': '100%', 'margin': '0 auto', 'padding': '2vh', 'border-radius': '0.5vh'}),

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
        percent_change=percent_change/100,
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
                                 [electricity_price_CO2_start,
                                     electricity_price_CO2_end],
                                 electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, capacity_factor_CO2/100
                                 )


if __name__ == '__main__':
    app.run_server(debug=True)
