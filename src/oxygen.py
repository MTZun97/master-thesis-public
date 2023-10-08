import variable as var
import pandas as pd
import numpy as np
import numpy_financial as npf
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from lcoh import lcoe,depreciation_table, CPI_df

def cash_flow(cap_factor, electrolyzer_cost, electricity_price, O2,
              electrolyzer_efficiency, mech_percent=0.3, elect_percent=0.2, water_rate = 0.00237495008,
              current_density=2, stack_percent=0.6, ASU_cost = 200, startup_year = 2021):
    
    elect_df= pd.DataFrame({"year": range(1983, 2100), "electricity_price": [electricity_price] * len(range(1983, 2100))}).set_index("year")
    CPI_inflator                       = CPI_df.loc[var.ref_year, "value"]/CPI_df.loc[var.basis_year, "value"]
    peak_production_rate               = round(var.average_production_rate * (1 + var.stack_oversize))   #kgH2/day
    total_active_area_with_degradation = round((peak_production_rate / 2.02) * (1000 / (24 * 3600)) * 2 * 
                                               (var.faradays_constant / (current_density * 100**2)))      #m2 (2.02-to moles, 2 = no. of electrodes, 100^2 = cm2 to m2)
    stack_electrical_usage             = 33.33/(electrolyzer_efficiency/100)
    electrolyzer_sys_cost                     = electrolyzer_cost/(total_active_area_with_degradation * electrolyzer_efficiency/100)
    
    
    stack_input_peak                   = (stack_electrical_usage / 24) * (peak_production_rate / 1000)                 #MW
    output_kgperday                    = peak_production_rate * cap_factor            #kgH2/day
    output_kgperyear                   = output_kgperday * 365              #kgH2/day
     
    stack_capital_cost                 = round(electrolyzer_sys_cost * stack_percent * total_active_area_with_degradation * 100**2)  
    mech_capital_cost                  = round(electrolyzer_sys_cost * mech_percent)   
    electrical_capital_cost            = round(electrolyzer_sys_cost * elect_percent)      
    stack_baseline_installed_cost      = round(stack_capital_cost * CPI_inflator *  var.elect_installed_factor)  
    mech_baseline_installed_cost       = round(mech_capital_cost * CPI_inflator * var.mech_installed_factor)  
    electrical_baseline_installed_cost = round(electrical_capital_cost * CPI_inflator *  var.elect_installed_factor)      
    direct_cap                         = (stack_baseline_installed_cost + mech_baseline_installed_cost +
                                        electrical_baseline_installed_cost)
    site_preparation                   = round(var.site_preparation_percent * direct_cap/(CPI_inflator),2)
    engineering_design                 = round(var.engineering_design_percent * direct_cap/(CPI_inflator),2)
    project_contingency                = round(var.project_contingency_percent * direct_cap/(CPI_inflator),2)
    upfront_permitting                 = round(var.upfront_permitting_percent * direct_cap/(CPI_inflator),2)
    depr_cap                           = round(direct_cap + ((site_preparation + engineering_design + project_contingency +
                                                              upfront_permitting) * CPI_inflator))

    
    land_cost                          = CPI_inflator * var.land_required * var.land_costperacre    
    total_cap                          = depr_cap + land_cost        
    labour_cost                        = var.total_plant_staff * var.labour_costperhour * var.work_hour
    overhead_GA_cost                   = labour_cost * var.overhead_rate
    property_tax_insurance_cost        = total_cap * var.tax_insurance_rate
    material_cost                      = (var.material_cost_percent * direct_cap/(CPI_inflator)) * CPI_inflator
    fixed_var_cost                     = round(labour_cost + overhead_GA_cost + property_tax_insurance_cost + 
                                               material_cost)

    
    inflation_factor                   = (1 + var.inflation_rate) ** (startup_year - var.ref_year)
    depr_cap_inflation                 = round(depr_cap * inflation_factor)
    non_dep_inflation                  = round(land_cost * inflation_factor)
    total_cap_investment_inflation     = round(depr_cap_inflation + non_dep_inflation)
    fixed_var_inflation                = round(fixed_var_cost * inflation_factor)
    decomissioning_inflation           = round(var.percent_decom * depr_cap_inflation)
    salvage_inflation                  = round(var.percent_salvage * total_cap_investment_inflation)

    
    #Cash Flow Analysis
    # 1. Time Series
    operation_year = [i for i in range(var.total_plant_life + 1)]
    actual_year = [i + startup_year - 1 for i in operation_year]
    analysis_year = [i + 1 for i in operation_year]
    
    # 2. Inflation price increase factor
    inflation_increase_factor = [(1 + var.inflation_rate) ** (i + startup_year - 1 - startup_year) for i in operation_year]

    #3. Replacement Cost and 4. Initial Equity Depreciable Capital
    unplanned_replacement_cost = -var.replace_factor * depr_cap
    specified_replacement_cost = [0 if i <= 1 else
                                  -(0.15 * direct_cap/ (CPI_inflator)) * CPI_inflator if (i-1) % var.stack_life == 0 else 0
                                  for i in operation_year]
    
    yearly_replacement_cost = [0 if i < 1 else (((unplanned_replacement_cost + specified_replacement_cost[i])* 
                              ((1 + var.inflation_rate) ** (startup_year - var.ref_year))) * inflation_increase_factor[i])
                             for i in operation_year]
    
    #4. Initial Equity Depreciable Capital
    initial_depr_capital_cost = [(-(depr_cap_inflation * inflation_increase_factor[i]) if i == 0 else 0)
                                  for i in operation_year]

    
    #5. Depreciation
    MACRS_df         = depreciation_table("20 years")
    annual_depr_cost = [0 if i == 0 else 
                        -sum(initial_depr_capital_cost) - yearly_replacement_cost[i] if i == 1 else 
                        -yearly_replacement_cost[i]
                       for i in operation_year]
    depr_cal_table = MACRS_df.apply(lambda x: x * annual_depr_cost, axis= 0)
    depr_cash_flow = [sum(np.diagonal(np.flipud(depr_cal_table), offset=i)) 
                      for i in range(-var.total_plant_life, len(MACRS_df.columns), 1)]
    depr_charge = [-depr_cash_flow[i] if i < 40 else -sum(depr_cash_flow[i:]) 
                   for i in range(0, var.total_plant_life + 1, 1)]

    #6. Salvage
    salvage = [0 if i < var.total_plant_life else inflation_increase_factor[i] * salvage_inflation for i in operation_year]
    
    #7. Other Non-Depreciable Capital Cost
    other_nondepr_cost = [-inflation_increase_factor[i] * non_dep_inflation if i == 0 else 0 for i in operation_year]
    
    #8. Other Variable Cost
    total_sys_electrical_usage = stack_electrical_usage * var.total_elect_usage_percent
    electricity_cost = [inflation_factor * total_sys_electrical_usage * var.price_conversion_factor * 
                                elect_df.loc[i, "electricity_price"] for i in actual_year]
    water_cost          = inflation_factor * var.process_water * water_rate
    other_variable_operating_cost = [ 0 if i < 1 else 
                                     -((electricity_cost[i] + water_cost) * output_kgperyear * 
                                       inflation_increase_factor[i] * var.percent_var) if i == 1 else
                                    - ((electricity_cost[i] + water_cost) * output_kgperyear * 
                                       inflation_increase_factor[i]) for i in operation_year]

    #9. Fixed Operating Cost
    fixed_operating_cost = [0 if i < 1 else
                           - fixed_var_inflation * inflation_increase_factor[i] * var.percent_fixed if i == 1 else
                           - fixed_var_inflation * inflation_increase_factor[i] for i in operation_year]


    #10. Cash from Working Capital Reserve 
    diff = lambda lst: [lst[i+1] - lst[i] for i in range(len(lst)-1)]
    working_capital_reserve = list(map(lambda i: var.working_cap * (fixed_operating_cost[i] + other_variable_operating_cost[i]), operation_year))
    cash_working_capital_reserve = [0] + diff(working_capital_reserve)
    cash_working_capital_reserve[-1] = -sum(cash_working_capital_reserve[:-1])
  
   
    #11. Hydrogen Sales
    hydrogen_sales = [0 if i < 1 else
                     output_kgperyear * var.percent_revs if i == 1 else
                     output_kgperyear for i in operation_year]

    
    #12. Decomission
    decomission = [- decomissioning_inflation * inflation_increase_factor[i] if i == var.total_plant_life else 0 
                  for i in operation_year]
    
    #13. Oxygen Sales
    oxygen_sales = [i * 8 for i in hydrogen_sales]
    oxygen_revenue = [i * O2 for i in hydrogen_sales]
    oxygen_capital_cost = [-ASU_cost*i/1000 for i in oxygen_sales]


    dict = {"actual_year": actual_year, "analysis_year": analysis_year, "operation_year": operation_year,
            "inflation_increase_factor": inflation_increase_factor, "initial_depr_capital_cost": initial_depr_capital_cost,
           "yearly_replacement_cost": yearly_replacement_cost, "cash_working_capital_reserve": cash_working_capital_reserve,
            "other_nondepr_cost": other_nondepr_cost, "salvage": salvage, "decomission": decomission, 
            "fixed_operating_cost": fixed_operating_cost,
            "other_variable_operating_cost": other_variable_operating_cost, "depreciation_charge": depr_charge,
           "hydrogen_sales": hydrogen_sales, "oxygen_sales": oxygen_sales, "oxygen_capital_cost": oxygen_capital_cost,
            "oxygen_revenue": oxygen_revenue}
    
    df = pd.DataFrame.from_dict(dict)

    
    # LCOH Calculation
    target_aftertax_nominal = ((1 + var.real_irr) * (1 + var.inflation_rate)) - 1
    total_tax_rate          = round(var.fed_tax_rate + (var.state_tax_rate * (1 - var.fed_tax_rate)),4)
    
    
    lcoh_initial_depreciable_capital = (npf.npv(target_aftertax_nominal,df["initial_depr_capital_cost"]))
    
    lcoh_yearly_replacement_cost = (npf.npv(target_aftertax_nominal,df["yearly_replacement_cost"]))
    
    lcoh_depreciation_charge = (npf.npv(target_aftertax_nominal,df["depreciation_charge"]))
    
    lcoh_other_nondepr_capital_cost = (npf.npv(target_aftertax_nominal,df["other_nondepr_cost"]))
    
    
    lcoh_salvage = (npf.npv(target_aftertax_nominal,df["salvage"]))
    
    lcoh_fixed_operating_cost = (npf.npv(target_aftertax_nominal,df["fixed_operating_cost"]))
    
    
    lcoh_other_variable_operating_cost = (npf.npv(target_aftertax_nominal,df["other_variable_operating_cost"]))
    
    lcoh_working_capital_reserve = (npf.npv(target_aftertax_nominal,df["cash_working_capital_reserve"]))
    
    lcoh_hydrogen_sales = (npf.npv(var.real_irr,df["hydrogen_sales"]))

    lcoh_decomission = (npf.npv(target_aftertax_nominal,df["decomission"]))
    
    lcoh_oxygen_sales = (npf.npv(var.real_irr,df["oxygen_sales"]))


    lcoh_oxygen_capital = (npf.npv(var.real_irr,df["oxygen_capital_cost"]))

    lcoh_oxygen_revenue = (npf.npv(var.real_irr,df["oxygen_revenue"]))
   

    #Final
    lcoh_H2_sales = lcoh_hydrogen_sales * (1 - total_tax_rate)
    
    lcoh_capital_costs = (- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) * 1) /lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
    
    lcoh_depreciation  = ((-(lcoh_depreciation_charge) * - total_tax_rate) /
                          lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor)
    
    lcoh_fixed_op_cost = (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)
                    * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
    
    lcoh_var_op_cost = (-(lcoh_other_variable_operating_cost)
                    * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
    
    lcoh_capital_costs_O2 = (- (lcoh_oxygen_capital) * 1) /lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
       
    
    lcoh_O2_revenue = (-(lcoh_oxygen_revenue)
            * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor   
    
    lcoh = np.round(lcoh_capital_costs + lcoh_depreciation + lcoh_fixed_op_cost + lcoh_var_op_cost, 3)
    lcoh_O2 = np.round(lcoh_capital_costs + lcoh_depreciation + lcoh_fixed_op_cost + lcoh_var_op_cost+
                    lcoh_capital_costs_O2  + lcoh_O2_revenue, 3)



    return lcoh, lcoh_O2

def create_O2revenue_plot(ASU_cost, electricity_price, electrolyzer_efficiency, 
                          electrolyzer_cost, capacity_factor, 
                          NG_price, O2_price = [0, 5]):
    
    O2_value = np.arange(O2_price[0], O2_price[1], 0.1).round(1)

    lcoh_O2_list = []
    lcoh_list = []
    for i in O2_value:
        lcoh, lcoh_O2 = cash_flow(cap_factor = capacity_factor, 
                                            electrolyzer_cost = electrolyzer_cost, electricity_price = electricity_price, 
                                            O2 = i, electrolyzer_efficiency = electrolyzer_efficiency, ASU_cost = ASU_cost)
        lcoh_O2_list.append(lcoh_O2)
        lcoh_list.append(lcoh)

    # SMR at gas price 10Euro/kg
    gas_price = [NG_price*10.8/1000] * len(O2_value)
    lcoh_smr  = [(i * 5.08) + 0.3918 for i in gas_price]



    data_dict = {"O2_price": O2_value, "LCOH - O2 Revenue": lcoh_O2_list, "LCOH": lcoh_list, "LCOH - SMR": lcoh_smr}

    df = pd.DataFrame.from_dict(data_dict).set_index("O2_price")
    
    fig = go.Figure()

    # Adding LCOH Line
    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH'],
                             mode='lines',
                             name='Green H<sub>2</sub>',
                             line=dict(color='#00CC96', width=4),
                             hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))

    # Adding LCOH - O2 Revenue Line
    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - O2 Revenue'],
                             mode='lines',
                             name='Green H<sub>2</sub> + O<sub>2</sub> Revenue',
                             line=dict(color='#FFA15A', width=4),
                             hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))

    # Adding LCOH - SMR Line
    fig.add_trace(go.Scatter(x=df.index, y=df['LCOH - SMR'],
                             mode='lines',
                             name='Grey H<sub>2</sub>',
                             line=dict(color='#7F7F7F', width=4),
                             hovertemplate='LCOH: %{y:.2f} $/kg<sub>H2</sub>'))

    fig.update_layout(
        yaxis=dict(
            title_text='LCOH ($/kg<sub>H<sub>2</sub></sub>)',
            title_font=dict(family='Arial, bold', size=20),
            tickfont=dict(family='Arial, bold', size=16),
        ),
        xaxis=dict(
            title_text='Oxygen Price ($/kg<sub>O<sub>2</sub></sub>)',
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

# df = create_O2revenue_plot(startup_year = 2020, ASU_cost = 200, electricity_price = 0.036, electrolyzer_efficiency= 80,
#                            electrolyzer_cost= 1000, capacity_factor= 0.8, NG_price = 10, O2_price = [0, 5])
# print(df)

# lcoh, lcoh_O2 =  cash_flow(startup_year = 2023, cap_factor = 0.8, electrolyzer_cost = 1000, electricity_price = 0.036, O2 = 0.1,
#               electrolyzer_efficiency = 80, mech_percent=0.3, elect_percent=0.2, water_rate = 0.00237495008,
#               current_density=2, stack_percent=0.6, ASU_cost = 200)

# print(lcoh, lcoh_O2)

# lcoh, _ = cash_flow(cap_factor = 0.6, electrolyzer_cost= 1000, 
#                     electricity_price = 0.036, O2 = 0, electrolyzer_efficiency = 70,
#                         mech_percent=0.3, elect_percent=0.2, water_rate = 0.00237495008, current_density=2, 
#                         stack_percent=0.6, ASU_cost = 200, startup_year = 2021)
# print(lcoh)