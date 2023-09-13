import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from lcoh import cash_flow
import plotly.express as px
import plotly.graph_objects as go

def sensitivity_analysis(percent_change=0.3, startup_year=2020, cap_factor=0.5, current_density=1.5,
           electrolzyer_cost=1000, electrolyzer_efficiency=50, stack_percent=0.6,
           mech_percent=0.2, elect_percent=0.2, water_rate=0.00237495008, elect_price=0.036):
    params = {
        "startup_year": startup_year,
        "cap_factor": cap_factor,
        "current_density": current_density,
        "stack_percent": stack_percent,
        "electrolyzer_cost": electrolzyer_cost,
        "electrolyzer_efficiency": electrolyzer_efficiency,
        "mech_percent": mech_percent,
        "elect_percent": elect_percent,
        "water_rate": water_rate,
        "elect_df": (pd.DataFrame.from_dict({"year": range(1983, 2100), "electricity_price": [elect_price] * len(range(1983, 2100))})
                     .set_index("year"))}

    params_low = {
        "startup_year": startup_year,
        "cap_factor": cap_factor * (1 + percent_change),
        "current_density": current_density,
        "stack_percent": stack_percent,
        "electrolyzer_cost": electrolzyer_cost * (1 - percent_change),
        "electrolyzer_efficiency": electrolyzer_efficiency * (1 + percent_change),
        "mech_percent": mech_percent,
        "elect_percent": elect_percent,
        "water_rate": water_rate * (1 - percent_change),
        "elect_df": (pd.DataFrame.from_dict({"year": range(1983, 2100), "electricity_price": [elect_price * (1 - percent_change)] * len(range(1983, 2100))})
                     .set_index("year"))}

    params_high = {
        "startup_year": startup_year,
        "cap_factor": cap_factor * (1 - percent_change),
        "current_density": current_density,
        "stack_percent": stack_percent,
        "electrolyzer_cost": electrolzyer_cost * (1 + percent_change),
        "electrolyzer_efficiency": electrolyzer_efficiency * (1 - percent_change),
        "mech_percent": mech_percent,
        "elect_percent": elect_percent,
        "water_rate": water_rate * (1 + percent_change),
        "elect_df": (pd.DataFrame.from_dict({"year": range(1983, 2100), "electricity_price": [elect_price * (1 + percent_change)] * len(range(1983, 2100))})
                     .set_index("year"))}

 

    lcoh_base = {}
    lcoh_low = {}
    lcoh_high = {}
    label_mapping = {
    "cap_factor": "Capacity Factor",
    "electrolyzer_cost": "Electrolyzer Cost",
    "electrolyzer_efficiency": "Electrolyzer Efficiency",
    "elect_df": "Electricity Cost",
    "water_rate": "Water Rate"
}


    keys = ["cap_factor", "electrolyzer_cost",
            "electrolyzer_efficiency", "elect_df", "water_rate"]
    variables = [
        params["cap_factor"],
        params["electrolyzer_cost"],
        params["electrolyzer_efficiency"],
        params["elect_df"],
        params["water_rate"]]

    for key, variable in zip(keys, variables):
        lcoh_base[key] = cash_flow(**params)[0]
        lcoh_low[key] = cash_flow(**{**params, key: params_low[key]})[0]
        lcoh_high[key] = cash_flow(**{**params, key: params_high[key]})[0]


    percentage_change = {key: {"low": (lcoh_low[key] - lcoh_base[key]) / lcoh_base[key] * 100,
                            "high": (lcoh_high[key] - lcoh_base[key]) / lcoh_base[key] * 100} for key in keys}


    ordered_keys = sorted(keys, key=lambda x: max(abs(percentage_change[x]["low"]), abs(percentage_change[x]["high"])), reverse=False)
    display_labels = [label_mapping[key] for key in ordered_keys]


    low_data = [percentage_change[key]["low"] for key in ordered_keys]
    high_data = [percentage_change[key]["high"] for key in ordered_keys]

    base_values = [lcoh_base[key] for key in ordered_keys]
    low_values = [lcoh_low[key] for key in ordered_keys]
    high_values = [lcoh_high[key] for key in ordered_keys]

    fig = go.Figure()


    fig.add_trace(go.Bar(
        y=display_labels,
        x=low_data,
        customdata=[(base, low) for base, low in zip(base_values, low_values)],
        hovertemplate='Percent Change: %{x:.2f}%<br>Base LCOH: %{customdata[0]:.2f}<br>Low LCOH: %{customdata[1]:.2f}',
        orientation='h',
        name='Low',
        marker=dict(
            color='rgba(76, 114, 176, 1)',
            line=dict(
                color='rgba(76, 114, 176, 1)',
                width=3)
        )
    ))


    fig.add_trace(go.Bar(
        y=display_labels,
        x=high_data,
        customdata=[(base, high) for base, high in zip(base_values, high_values)],
        hovertemplate='Percent Change: %{x:.2f}%<br>Base LCOH: %{customdata[0]:.2f}<br>High LCOH: %{customdata[1]:.2f}',
        orientation='h',
        name='High',
        marker=dict(
            color='rgba(196, 57, 50, 1)',
            line=dict(
                color='rgba(196, 57, 50, 1)',
                width=3)
        )
    ))


    fig.update_layout(
        title='<b>Sensitivity Analysis of Green Hydrogen Production Cost<b>',
        xaxis_title='Percentage Change in LCOH (%)',
        yaxis_title='Parameters',
        yaxis=dict(
            tickvals=list(range(len(ordered_keys))),
        ),
        barmode='relative', showlegend=False, title_x=0.5, 
        title_font=dict(size=18, family='Arial Bold', color='black')
    )


    return fig
