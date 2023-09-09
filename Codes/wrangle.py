import pandas as pd
from index import CPI_df, currency
from conversion import calc_new_efficiency, calc_new_sys_size, get_country_name

def wrangle_electrolyzers(filepath):
    
    #Cost Data Collection
    data = pd.read_excel(filepath, header = 0, sheet_name = "database")
    data = data[["no", "method","electrolyser_type", "reference_year", "year_of_estimate", "cost", "cost_unit", "efficiency", "efficiency_unit", 
         "system_size", "system_size_unit"]]
    data.drop(data[data["cost"].isnull()].index, inplace = True)
    
    temp_data1 = pd.merge(data, CPI_df, left_on="reference_year", right_on="year")
    temp_data1["cost_2021"] = temp_data1["cost"]*temp_data1["CPI_conversion"]    
    temp_data2 = pd.merge(temp_data1, currency, left_on = "cost_unit", right_on = "currency")
    temp_data2["cost_2021USD/kW"] = temp_data2["cost_2021"] * temp_data2["currency_value"]
    temp_data2.drop(columns = ['value','CPI_conversion', 'cost_2021', 'currency', 'currency_value'], inplace = True)
    
    e = temp_data2[temp_data2["efficiency"].notnull()]
    temp_data2["efficiency_LHV"] = e.apply(lambda x: calc_new_efficiency(x["efficiency"], x["efficiency_unit"]), axis=1)
    temp_data2.drop(columns = ["efficiency", "efficiency_unit"], inplace = True)
    
    s = temp_data2[temp_data2["system_size"].notnull()]
    temp_data2["system_size_kW"] = s.apply(lambda x: calc_new_sys_size(x["system_size"], x["system_size_unit"]), axis=1)
    temp_data2.drop(columns = ["system_size", "system_size_unit"], inplace = True)
    temp_data2["year_of_estimate"] = temp_data2["year_of_estimate"].astype(int)
    
    # Subsetting dataframe into Alkaline, PEM and SOEC
    alk      = (temp_data2[temp_data2["electrolyser_type"] == "Alkaline"].
                sort_values("year_of_estimate").
                drop(columns = ["electrolyser_type"]))
    pem      = (temp_data2[temp_data2["electrolyser_type"] == "PEM"].
                sort_values("year_of_estimate").
                drop(columns = ["electrolyser_type"]))
    soec      = (temp_data2[temp_data2["electrolyser_type"] == "SOEC"].
                sort_values("year_of_estimate").
                drop(columns = ["electrolyser_type"]))
    return temp_data2, alk, pem, soec
electrolyzers, alk, pem, soec = wrangle_electrolyzers("excel/Reference.xlsx")

def wrangle_iea(filepath):
    # IEA Database
    iea_data = pd.read_excel(filepath, header = 0, sheet_name = "iea_project")
    iea_data = iea_data[(iea_data["product"] == "H2") ]
    iea_data = iea_data[(iea_data["technology"] == "ALK") | (iea_data["technology"] == "PEM") | 
                        (iea_data["technology"] == "SOEC") | (iea_data["technology"] == "Other Electrolysis")]
    iea_data = iea_data[iea_data["announced_size"].notnull()]
    iea_data.drop(columns = [ "normalized_capacity_nm2H2/h", "product", "normalized_capacity_ktH2/y"], inplace = True)
    iea_data = iea_data[iea_data["country"].notnull()]
    iea_data["country"] = [c[:3] for c in iea_data["country"]]
    # apply the function to the ISO3 column and store the result in a new column
    iea_data['country_converted'] = iea_data['country'].apply(get_country_name)
    
    iea_alk = pd.DataFrame(iea_data[(iea_data["technology"] == "ALK")].groupby("date_online")["normalized_capacity_Mwel"].sum())
    iea_pem = pd.DataFrame(iea_data[(iea_data["technology"] == "PEM")].groupby("date_online")["normalized_capacity_Mwel"].sum())
    new_index_alk = pd.RangeIndex(start=1992, stop=2031)
    new_index_pem = pd.RangeIndex(start=2000, stop=2031)
    iea_alk = iea_alk.reindex(new_index_alk).fillna(0)
    iea_pem = iea_pem.reindex(new_index_pem).fillna(0)
    iea_alk = iea_alk.reset_index()
    iea_pem = iea_pem.reset_index()
    iea_alk = iea_alk.rename(columns={'index': 'date_online'})
    iea_pem = iea_pem.rename(columns={'index': 'date_online'})
    iea_alk["cumulative_capacity_MWel"] = iea_alk["normalized_capacity_Mwel"].cumsum()
    iea_pem["cumulative_capacity_MWel"] = iea_pem["normalized_capacity_Mwel"].cumsum()
    
    return iea_data, iea_alk, iea_pem
iea_data, iea_alk, iea_pem = wrangle_iea("excel/Reference.xlsx")

def wrangle_manufacturers(filepath):
    manufacturer_data = pd.read_excel(filepath, header = 0, sheet_name = "manufacturer")  
    manufacturer_data['headquarter'] = manufacturer_data['headquarter'].apply(get_country_name)
    return manufacturer_data
manufacturer_data = wrangle_manufacturers("excel/Reference.xlsx")

