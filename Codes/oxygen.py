import variable as var
import pandas as pd
import numpy as np
import numpy_financial as npf
import seaborn as sns
import matplotlib.pyplot as plt
from index import lcoe,depreciation_table, CPI_df

def cash_flow(startup_year, cap_factor, current_density, stack_percent, electrolyzer_cost, 
              electrolyzer_efficiency, elect_df, mech_percent, elect_percent, O2, water_rate = 0.00237495008):
    
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
    
    dict = {"actual_year": actual_year, "analysis_year": analysis_year, "operation_year": operation_year,
            "inflation_increase_factor": inflation_increase_factor, "initial_depr_capital_cost": initial_depr_capital_cost,
           "yearly_replacement_cost": yearly_replacement_cost, "cash_working_capital_reserve": cash_working_capital_reserve,
            "other_nondepr_cost": other_nondepr_cost, "salvage": salvage, "decomission": decomission, 
            "fixed_operating_cost": fixed_operating_cost,
            "other_variable_operating_cost": other_variable_operating_cost, "depreciation_charge": depr_charge,
           "hydrogen_sales": hydrogen_sales, "oxygen_sales": oxygen_sales}
    
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
    
    lcoh_oxygen_sales = (npf.npv(var.real_irr,df["hydrogen_sales"]))
   

    #Final
    lcoh_H2_sales = lcoh_hydrogen_sales * (1 - total_tax_rate)
    lcoh_O2_sales = lcoh_oxygen_sales * (1 - total_tax_rate) * O2
    lcoh_capital_costs = (- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) * 1) /lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
    
    lcoh_depreciation  = ((-(lcoh_depreciation_charge) * - total_tax_rate) /
                          lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor)
    
    lcoh_fixed_op_cost = (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)
                    * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
    
    lcoh_var_op_cost = (-(lcoh_other_variable_operating_cost)
                    * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
       
    lcoh = round(lcoh_capital_costs + lcoh_depreciation + lcoh_fixed_op_cost + lcoh_var_op_cost, 3)
    

    #Oxygen as By Product  
    lcoh_var_op_cost_O2 = (-(lcoh_other_variable_operating_cost + lcoh_O2_sales)
                    * (1 - total_tax_rate))/lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor
       
    lcoh_O2_byproduct = round(lcoh_capital_costs + lcoh_depreciation + lcoh_fixed_op_cost + lcoh_var_op_cost_O2, 3)
    
    #Oxygen production - Mass allocation
    lcoh_O2_mass = round((((- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) ) + ((-(lcoh_depreciation_charge) * - total_tax_rate)) + 
                 (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)* (1 - total_tax_rate)) + 
                 (-(lcoh_other_variable_operating_cost) * (1 - total_tax_rate))) * (1/9) /
                 lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor),3)
    
    lcoo_O2_mass = round((((- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) ) + ((-(lcoh_depreciation_charge) * - total_tax_rate)) + 
                 (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)* (1 - total_tax_rate)) + 
                 (-(lcoh_other_variable_operating_cost) * (1 - total_tax_rate))) * (8/9) /
                 lcoh_O2_sales * (1+ var.inflation_rate)**1/inflation_factor),3)
    
    #Oxygen production - cost allocation
    lcoo_assumed = 0.1
    lcoh_assumed = 2
    lcoh_lcoo = lcoo_assumed + lcoh_assumed
    lcoh_O2_cost = round((((- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) ) + ((-(lcoh_depreciation_charge) * - total_tax_rate)) + 
                 (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)* (1 - total_tax_rate)) + 
                 (-(lcoh_other_variable_operating_cost) * (1 - total_tax_rate))) * (lcoh_assumed/lcoh_lcoo) /
                 lcoh_H2_sales * (1+ var.inflation_rate)**1/inflation_factor),3)
    
    lcoo_O2_cost = round((((- (lcoh_initial_depreciable_capital + lcoh_yearly_replacement_cost + lcoh_working_capital_reserve + 
                          lcoh_other_nondepr_capital_cost) ) + ((-(lcoh_depreciation_charge) * - total_tax_rate)) + 
                 (-(lcoh_fixed_operating_cost + lcoh_decomission + lcoh_salvage)* (1 - total_tax_rate)) + 
                 (-(lcoh_other_variable_operating_cost) * (1 - total_tax_rate))) * (lcoo_assumed/lcoh_lcoo) /
                 lcoh_O2_sales * (1+ var.inflation_rate)**1/inflation_factor),3)
    
    return lcoh, lcoh_O2_byproduct, lcoh_O2_mass, lcoo_O2_mass, lcoh_O2_cost, lcoo_O2_cost



#Electrolysis
O2_value = np.arange(0, 4.5, 0.5).round(1)
df = pd.read_csv("excel/cost_reduction.csv", index_col=0)
pem_cost = df.loc[2021, "pem_doublef_sl"]
pem_eff  = df.loc[2021, "eff_singlef_pem"]
lcoh_pem_CF20 = []
lcoh_pem_CF50 = []
lcoh_pem_CF80 = []
lcoh, lcoh_O2_byproduct, lcoh_O2_mass, lcoo_O2_mass, lcoh_O2_cost, lcoo_O2_cost = cash_flow(startup_year= 2020, cap_factor= 0.5, current_density=0.25, 
                                                                stack_percent= 0.5,
                                                         electrolyzer_cost= pem_cost, electrolyzer_efficiency= pem_eff, mech_percent = 0.2,
                                                         elect_percent = 0.3, O2 = 1.4,
                                                         elect_df= pd.DataFrame({"year": range(1983, 2100), "electricity_price": [0.05] * 
                                                                                 len(range(1983, 2100))}).set_index("year"))

for i in O2_value:
    lcoh, lcoh_O2_byproduct, _, _, _, _ = cash_flow(startup_year= 2020, cap_factor= 0.2, current_density=2, stack_percent= 0.5,
                                                         electrolyzer_cost= pem_cost, electrolyzer_efficiency= pem_eff, 
                                                         mech_percent = 0.2, elect_percent = 0.3, O2 = i,
                                                         elect_df= pd.DataFrame({"year": range(1983, 2100), "electricity_price": [0.05] * 
                                                                                 len(range(1983, 2100))}).set_index("year"))
    lcoh_pem_CF20.append(lcoh_O2_byproduct)

for i in O2_value:
    lcoh, lcoh_O2_byproduct, _, _, _, _ = cash_flow(startup_year= 2020, cap_factor= 0.5, current_density=2, stack_percent= 0.5,
                                                         electrolyzer_cost= pem_cost, electrolyzer_efficiency= pem_eff, 
                                                         mech_percent = 0.2, elect_percent = 0.3, O2 = i,
                                                         elect_df= pd.DataFrame({"year": range(1983, 2100), "electricity_price": [0.05] * 
                                                                                 len(range(1983, 2100))}).set_index("year"))
    lcoh_pem_CF50.append(lcoh_O2_byproduct)

for i in O2_value:
    lcoh, lcoh_O2_byproduct, _, _, _, _ = cash_flow(startup_year= 2020, cap_factor= 0.8, current_density=2, stack_percent= 0.5,
                                                         electrolyzer_cost= pem_cost, electrolyzer_efficiency= pem_eff, 
                                                         mech_percent = 0.2, elect_percent = 0.3, O2 = i,
                                                         elect_df= pd.DataFrame({"year": range(1983, 2100), "electricity_price": [0.05] * 
                                                                                 len(range(1983, 2100))}).set_index("year"))
    lcoh_pem_CF80.append(lcoh_O2_byproduct)

# SMR at gas price 10Euro/kg
gas_price_low = [0.115] * len(O2_value)
lcoh_smr_low  = [(i * 5.08) + 0.3918 for i in gas_price_low]

# SMR at gas price 30Euro/kg
gas_price_high = [0.345] * len(O2_value)
lcoh_smr_high  = [(i * 5.08) + 0.3918 for i in gas_price_high]



dict = {"O2_price": O2_value, "Capacity Factor 20%": lcoh_pem_CF20, "Capacity Factor 50%": lcoh_pem_CF50,
        "Capacity Factor 80%": lcoh_pem_CF80,"LCOH - SMR (10 Euro/MWh)": lcoh_smr_low, "LCOH - SMR (30 Euro/Mwh)": lcoh_smr_high}

lcoh_comp = pd.DataFrame.from_dict(dict).set_index("O2_price")



sns.set_theme("white")
sns.color_palette("deep")
plt.figure(figsize=(16, 7))
for column in lcoh_comp.columns:
    if column.startswith("LCOH - SMR"):
        # Use the same line color for lcoh_smr_low and lcoh_smr_high
        sns.lineplot(data=lcoh_comp, x=lcoh_comp.index, y=column, label=column, 
                     color= (0.7686274509803922, 0.3058823529411765, 0.3215686274509804), legend = False)
        
        # Add text annotations for gas prices
        gas_price = column.split("(")[-1].split(")")[0]  # Extract gas price from column name
        plt.text(lcoh_comp.index[-1], lcoh_comp[column].iloc[-1], gas_price, 
                 color= (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
                 ha='left', va='center')
    else:
        sns.lineplot(data=lcoh_comp, x=lcoh_comp.index, y=column, label=column)


# Add shaded area between lcoh_smr_low and lcoh_smr_high
plt.fill_between(lcoh_comp.index, lcoh_comp["LCOH - SMR (10 Euro/MWh)"], lcoh_comp["LCOH - SMR (30 Euro/Mwh)"], alpha=0.2, 
                 color=(0.7686274509803922, 0.3058823529411765, 0.3215686274509804))

plt.xticks(O2_value, O2_value, rotation=90, fontsize=12, fontweight='bold')
plt.yticks(fontsize=12, fontweight='bold')
plt.xlabel('Oxygen Selling Price (USD/kgO2)', fontsize=16, fontweight="bold", font="Arial")
plt.ylabel('LCOH [USD/kgH2]', fontsize=16, fontweight="bold", font="Arial")
plt.grid(linestyle="dashed", linewidth=1, alpha=0.6)
plt.savefig("figures/lcoh_O2", dpi=300, bbox_inches='tight')

plt.show()