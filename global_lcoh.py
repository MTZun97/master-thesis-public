import pandas as pd
from lcoh import cash_flow
import plotly.graph_objects as go
from lcoh import lcoe, lcoe_constant, valid_sources

df = pd.read_csv("data/cost_reduction.csv", index_col=0)


def capacity_factor(offshore_wind_lcoe=0.23, solar_lcoe=0.12, onshore_wind_lcoe=0.23):
    return {
        "offshore_wind_lcoe": offshore_wind_lcoe,
        "solar_lcoe": solar_lcoe,
        "onshore_wind_lcoe": onshore_wind_lcoe
    }


cap_factor_sources = capacity_factor()
settings = {
    'low': {'alk': {'params': {"current_density": 0.2, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef_sl", 'eff': "eff_singlef_alk"},
            'pem': {'params': {"current_density": 1, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef_sl", 'eff': "eff_singlef_pem"}},
    'high': {'alk': {'params': {"current_density": 0.6, "stack_percent": 0.5, "mech_percent": 0.2, "elect_percent": 0.3}, 'cost': "alk_doublef", 'eff': "eff_singlef_alk"},
             'pem': {'params': {"current_density": 2, "stack_percent": 0.6, "mech_percent": 0.3, "elect_percent": 0.2}, 'cost': "pem_doublef", 'eff': "eff_singlef_pem"}}
}

lcoh_data = {}


def calculate_data(setting_type):
    for tech_type in ['alk', 'pem']:
        data = []
        setting = settings[setting_type][tech_type]
        for index in df.index:
            electrolyzer_cost = df.loc[index, setting['cost']]
            electrolyzer_efficiency = df.loc[index, setting['eff']]
            lcoh_row = {"Index": index}
            for source in valid_sources:
                cap_factor = cap_factor_sources.get(source, 0.8)
                lcoh, _, _, _ = cash_flow(startup_year=index, cap_factor=cap_factor, electrolyzer_cost=electrolyzer_cost, electrolyzer_efficiency=electrolyzer_efficiency, elect_df=lcoe(
                    source, "World") if setting_type == 'low' else lcoe_constant(source, "World"), **setting['params'])
                lcoh_row[source] = lcoh
            data.append(lcoh_row)
        lcoh_data[f"{setting_type}_{tech_type}"] = pd.DataFrame(
            data).set_index('Index')


def global_lcoh(electrolyzer_type="alk"):
    fig = go.Figure()

    calculate_data('low')
    calculate_data('high')

    lcoh_data['average_alk'] = (
        lcoh_data['low_alk'] + lcoh_data['high_alk']) / 2
    lcoh_data['average_pem'] = (
        lcoh_data['low_pem'] + lcoh_data['high_pem']) / 2

    sources = ['offshore_wind_lcoe', 'solar_lcoe', 'onshore_wind_lcoe']
    source_names = ['Offshore Wind LCOH', 'Solar LCOH', 'Onshore Wind LCOH']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    for idx, source in enumerate(sources):
        legend_group = f"group_{idx}"

        fig.add_trace(go.Scatter(
            x=lcoh_data[f'low_{electrolyzer_type}'].index.tolist(
            ) + lcoh_data[f'high_{electrolyzer_type}'].index.tolist()[::-1],
            y=lcoh_data[f'low_{electrolyzer_type}'][source].tolist(
            ) + lcoh_data[f'high_{electrolyzer_type}'][source].tolist()[::-1],
            fill='toself',
            fillcolor=f'rgba({int(colors[idx][1:3], 16)}, {int(colors[idx][3:5], 16)}, {int(colors[idx][5:7], 16)}, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            legendgroup=legend_group,
        ))

        fig.add_trace(go.Scatter(
            x=lcoh_data[f'average_{electrolyzer_type}'].index,
            y=lcoh_data[f'average_{electrolyzer_type}'][source],
            mode='lines',
            line=dict(color=colors[idx]),
            name=source_names[idx],
            legendgroup=legend_group,
        ))

    title = f"<b>Global Levelized Cost of Hydrogen for {'Alkaline' if electrolyzer_type == 'alk' else 'PEM'} Electrolyzers<b>"

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title="Levelized Cost of Hydrogen", title_x=0.5,
        title_font=dict(size=18, family='Arial Bold', color='black'), legend=dict(xanchor="right", x=0.99, yanchor="top", y=0.99)
    )

    return fig

    # fig.update_layout(
    #     xaxis_title_font=dict(size=16),
    #     yaxis_title_font=dict(size=16),
    #     xaxis=dict(tickangle=90, tickfont=dict(size=12)),
    #     yaxis=dict(tickfont=dict(size=12)),
    #     legend=dict(xanchor="right", x=0.99, yanchor="top", y=0.99),
    #     showlegend=True,
    #     plot_bgcolor="#E6E6FA",
    #     title_text="<b>Electrolyzer Manufacturers by Country</b>",
    #     title_x=0.5,
    #     title_font=dict(size=18, family='Arial', color='black'),
    #     margin=dict(b=50)
    # )
