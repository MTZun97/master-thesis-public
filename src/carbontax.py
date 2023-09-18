import pandas as pd
import numpy as np
from oxygen import cash_flow
import matplotlib.pyplot as plt
import plotly.express as px

def create_carbontax_plot(NG_price, CCUS_percent, capture_rate, carbon_tax, electricity_price_CO2, 
                          electrolyzer_efficiency_CO2, electrolyzer_cost_CO2, capacity_factor_CO2):
    
    electricity_price_CO2 = np.arange(electricity_price_CO2[0], electricity_price_CO2[1], 0.01).round(3)

    gas_price = [NG_price*10.8/1000] * len(electricity_price_CO2)
    lcoh_smr  = [(i * 5.08) + 0.3918 for i in gas_price]
    lcoh_smr_ccus = [i* (1 + CCUS_percent/100) for i in lcoh_smr]
    lcoh_smr_tax = [i + carbon_tax/100 for i in lcoh_smr]
    lcoh_smr_ccus_tax = [i + ((carbon_tax/100) * (1-capture_rate/100)) for i in lcoh_smr]

    lcoh_list = []
    for i in electricity_price_CO2:
        lcoh, _ = cash_flow(cap_factor = capacity_factor_CO2, electrolyzer_cost= electrolyzer_cost_CO2, 
                            electricity_price = i, O2 = 0, electrolyzer_efficiency = electrolyzer_efficiency_CO2,
                             mech_percent=0.3, elect_percent=0.2, water_rate = 0.00237495008, current_density=2, 
                             stack_percent=0.6, ASU_cost = 200, startup_year = 2021)
        lcoh_list.append(lcoh)

    data_dict = {"electricity_price": electricity_price_CO2, "LCOH": lcoh_list, "LCOH - SMR": lcoh_smr, 
            "LCOH - SMR + CCUS": lcoh_smr_ccus, "LCOH - SMR + Carbon Tax": lcoh_smr_tax,
            "LCOH - SMR + CCUS + Carbon Tax": lcoh_smr_ccus_tax}

    df = pd.DataFrame.from_dict(data_dict).set_index("electricity_price")

    fig = px.line(df, x=df.index, y=df.columns)

    # Adding labels and title
    fig.update_xaxes(title_text='Electricity Price ($/kWh)')
    fig.update_yaxes(title_text='LCOH ($/kgH2)')

    fig.update_layout(
        title=dict(
            text='<b>LCOH comparison: green, grey, and blue hydrogen<b>',
            y=0.95, 
            x=0.5,  
            xanchor='center',  
            yanchor='top',
            font=dict(
                family="Arial Bold",
                size=20,
                color="black"
            ),  
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
                size=12,
                color="black"
            ),
            bordercolor="Black",
            borderwidth=2,
            itemsizing='constant'
        ),
        legend_title_text='',
        margin=dict(
            t=100,  
        )
    )

    return fig



