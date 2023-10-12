import pandas as pd
import numpy as np
from oxygen import cash_flow
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def create_carbontax_plot(NG_price, CCUS_percent, capture_rate, carbon_tax, 
                          electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, capacity_factor_CO2, electricity_price_CO2= [0, 100]):
    
    electricity_price_CO2 = np.arange(electricity_price_CO2[0], electricity_price_CO2[1], 5).round(3)

    gas_price = [NG_price*10.8/1000] * len(electricity_price_CO2)
    lcoh_smr  = [(i * 5.08) + 0.3918 for i in gas_price]
    lcoh_smr_ccus = [i* (1 + CCUS_percent/100) for i in lcoh_smr]
    lcoh_smr_tax = [i + carbon_tax/100 for i in lcoh_smr]
    lcoh_smr_ccus_tax = [i + ((carbon_tax/100) * (1-capture_rate/100)) for i in lcoh_smr_ccus]

    lcoh_list = []
    for i in electricity_price_CO2:
        lcoh, _ = cash_flow(cap_factor = capacity_factor_CO2, electrolyzer_cost= electrolyzer_cost_CO2, 
                            electricity_price = i/1000, O2 = 0, electrolyzer_efficiency = electrolyzer_efficiency_CO2,
                             mech_percent=0.3, elect_percent=0.2, water_rate = 0.00237495008, current_density=2, 
                             stack_percent=0.6, startup_year = 2021)
        lcoh_list.append(lcoh)

    data_dict = {"electricity_price": electricity_price_CO2, "LCOH": lcoh_list, "LCOH - SMR": lcoh_smr, 
            "LCOH - SMR + CCUS": lcoh_smr_ccus, "LCOH - SMR + Carbon Tax": lcoh_smr_tax,
            "LCOH - SMR + CCUS + Carbon Tax": lcoh_smr_ccus_tax}

    df = pd.DataFrame.from_dict(data_dict).set_index("electricity_price")

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH'], mode='lines', 
                            name='Green H<sub>2</sub>',
                            line=dict(color='#00CC96', width=4),
                            hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))  # Adjust the width here

    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - SMR'], mode='lines', 
                            name='Grey H<sub>2</sub>',
                            line=dict(color='#7f7f7f', width=4),
                            hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))  # Adjust the width here

    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - SMR + Carbon Tax'], mode='lines', 
                            name='Grey H<sub>2</sub> + Carbon Tax',
                            line=dict(color='#7f7f7f', width=4, dash='dashdot'),
                            hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))  # Adjust the width here

    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - SMR + CCUS'], mode='lines', 
                            name='Blue H<sub>2</sub>',
                            line=dict(color='#636EFA', width=4),
                            hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))  # Adjust the width here

    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - SMR + CCUS + Carbon Tax'], mode='lines', 
                            name='Blue H<sub>2</sub> + Carbon Tax',
                            line=dict(color='#636EFA', width=4, dash='dashdot'),
                            hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))  # Adjust the width here

    fig.update_layout(
        yaxis=dict(
            title_text='LCOH ($/kg<sub>H<sub>2</sub></sub>)',
            title_font=dict(family='Arial, bold', size=20),
            tickfont=dict(family='Arial, bold', size=16),
        ),
        xaxis=dict(
            title_text='Electricity Price ($/MWh)',
            title_font=dict(family='Arial, bold', size=20),
            tickfont=dict(family='Arial, bold', size=16),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(
                family="Arial Bold",
                size=16,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
            itemsizing='constant'
        ),
        legend_title_text='',
        margin=dict(
            t=50,  
        )
    )

    return fig



