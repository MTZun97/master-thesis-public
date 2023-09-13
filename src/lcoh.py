import variable as var
import pandas as pd
import numpy as np
import numpy_financial as npf

# Inflation Calculation
CPI_dict = {"year": range(1990, 2022, 1), "value": [8.1, 9, 7.6, 7.1, 10.2, 9.1, 6.5, 5.6, 5.1, 3, 3.4, 3.8, 2.9,
                                                    3, 3.5, 4.1, 4.3, 4.8, 8.9, 2.9, 3.3, 4.8, 3.7, 2.6, 2.3,1.4, 
                                                    1.6, 2.2, 2.4, 2.2, 1.9, 3.5]}
CPI_df   = pd.DataFrame.from_dict(CPI_dict).set_index("year")
CPI_df["CPI_conversion"]  = CPI_df["value"] / CPI_df["value"].iloc[-1]
currency_rates         = {'USD/kW': 1, 'Euro/kW': 1.09}
currency               = pd.DataFrame.from_dict({"currency": currency_rates.keys(), "currency_value": currency_rates.values()})

# Depreciation Calculation
MACRS_dict = {"recovery_period": range(1, 22, 1),
              "3 years" : [0.3333, 0.4445, 0.1481, 0.0741],
              "5 years" : [0.2, 0.32, 0.192, 0.1152, 0.1152, 0.576],
              "7 years" : [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446],
              "10 years": [0.1, 0.18, 0.144, 0.1152, 0.0922, 0.0737, 0.0655, 0.0655, 0.0656, 0.0655, 0.0328],
              "15 years": [0.05, 0.095, 0.0855, 0.077, 0.0693, 0.0623, 0.059, 0.059, 0.0591, 0.059, 0.0991, 0.059, 0.0591, 0.059,
                           0.0591,0.0295],
              "20 years": [0.0375, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285, 0.04888, 0.04522, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462,
                        0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461, 0.02231]}
def depreciation_table(year):
    MACRS_df = pd.DataFrame.from_dict(MACRS_dict[year])
    MACRS_df = MACRS_df.T
    MACRS_df = pd.concat([pd.DataFrame(np.zeros((1, len(MACRS_df.columns)))), 
                      pd.concat([MACRS_df]*var.total_plant_life, ignore_index=True)], ignore_index=True)
    return MACRS_df


# Levelized Cost of Energy Calculation
valid_sources = ["offshore_wind_lcoe", "solar_lcoe", "onshore_wind_lcoe"]

# For Optimistic Scneario
def lcoe(source, location):
    if source not in valid_sources:
        raise ValueError(f"Invalid source. Available sources: {valid_sources}")

    lcoe_df = pd.read_csv("src\data\lcoe.csv")
    lcoe_df = lcoe_df[lcoe_df["entity"] == location].sort_values("year")

    # Create a DataFrame with a complete range of years
    complete_years = pd.DataFrame({"year": range(1990, 2101)})

    # Merge the complete years with the original DataFrame
    lcoe_df = pd.merge(complete_years, lcoe_df, on="year", how="left")

    df = lcoe_df[["year", source]].set_index("year")

    if source == "solar_lcoe":
        avg_pct_change = df[df[source].notnull()][source][-3:].pct_change().mean()
    else: 
        avg_pct_change = df[df[source].notnull()][source].pct_change().mean()

    # Find the year where the null values start
    start_year = df.loc[df[source].isna()].index.min()

    # If start_year is less than 2021, set it to 2021
    start_year = max(2021, start_year)
    # Backward fill the values for years from 1990 to the start year
    df.loc[:start_year] = df.loc[:start_year].bfill()
    
    # Project future values as per the average percentage change
    for i in range(start_year, 2101):
        df.loc[i, source] = df.loc[i-1, source] * (1 + avg_pct_change)

    df = df.rename(columns={source: "electricity_price"})
    return df
# For Pessimistic Scneario
def lcoe_constant(source, location):
    if source not in valid_sources:
        raise ValueError(f"Invalid source. Available sources: {valid_sources}")

    lcoe_df = pd.read_csv("src\data\lcoe.csv")
    lcoe_df = lcoe_df[lcoe_df["entity"] == location].sort_values("year")

    # Create a DataFrame with a complete range of years
    complete_years = pd.DataFrame({"year": range(1990, 2101)})

    # Merge the complete years with the original DataFrame
    lcoe_df = pd.merge(complete_years, lcoe_df, on="year", how="left")

    lcoe_df = lcoe_df.where(lcoe_df["year"] <= 2021, lcoe_df.ffill())
    lcoe_df = lcoe_df.where(lcoe_df["year"] > 2021, lcoe_df.bfill())
    
    df = lcoe_df[["year", source]].set_index("year").rename(columns = {source: "electricity_price"})

    return df


def cash_flow(startup_year, cap_factor, current_density, stack_percent, electrolyzer_cost, 
              electrolyzer_efficiency, elect_df, mech_percent, elect_percent, water_rate = 0.00237495008):
    
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
                                  -(stack_percent * direct_cap/ (CPI_inflator)) * CPI_inflator if (i-1) % var.stack_life == 0 else 0
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
    depr_charge = [-depr_cash_flow[i] if i < var.total_plant_life else -sum(depr_cash_flow[i:]) 
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
    
    
    dict = {"actual_year": actual_year, "analysis_year": analysis_year, "operation_year": operation_year,
            "inflation_increase_factor": inflation_increase_factor, "initial_depr_capital_cost": initial_depr_capital_cost,
           "yearly_replacement_cost": yearly_replacement_cost, "cash_working_capital_reserve": cash_working_capital_reserve,
            "other_nondepr_cost": other_nondepr_cost, "salvage": salvage, "decomission": decomission, 
            "fixed_operating_cost": fixed_operating_cost,
            "other_variable_operating_cost": other_variable_operating_cost, "depreciation_charge": depr_charge,
           "hydrogen_sales": hydrogen_sales}
    
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
       
    lcoh = round(lcoh_capital_costs + lcoh_depreciation + lcoh_fixed_op_cost + lcoh_var_op_cost, 3)

    return lcoh, lcoh_capital_costs,lcoh_depreciation , lcoh_fixed_op_cost, lcoh_var_op_cost
