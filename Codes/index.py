import pandas as pd
import numpy as np
import variable as var


# Inflation Calculation
CPI_dict = {"year": range(1990, 2022, 1), "value": [8.1, 9, 7.6, 7.1, 10.2, 9.1, 6.5, 5.6, 5.1, 3, 3.4, 3.8, 2.9,
                                                    3, 3.5, 4.1, 4.3, 4.8, 8.9, 2.9, 3.3, 4.8, 3.7, 2.6, 2.3,1.4, 
                                                    1.6, 2.2, 2.4, 2.2, 1.9, 3.5]}
CPI_df   = pd.DataFrame.from_dict(CPI_dict).set_index("year")
CPI_df["CPI_conversion"]  = CPI_df["value"] / CPI_df["value"].iloc[-1]

# Currency Exchange Calculation
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
valid_sources = ["bioenergy_lcoe", "offshore_wind_lcoe", "solar_lcoe",
                 "hydro_lcoe", "onshore_wind_lcoe"]

# For Optimistic Scneario

def lcoe(source, location):
    if source not in valid_sources:
        raise ValueError(f"Invalid source. Available sources: {valid_sources}")

    lcoe_df = pd.read_csv("excel/lcoe.csv")
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

    lcoe_df = pd.read_csv("excel/lcoe.csv")
    lcoe_df = lcoe_df[lcoe_df["entity"] == location].sort_values("year")

    # Create a DataFrame with a complete range of years
    complete_years = pd.DataFrame({"year": range(1990, 2101)})

    # Merge the complete years with the original DataFrame
    lcoe_df = pd.merge(complete_years, lcoe_df, on="year", how="left")

    lcoe_df = lcoe_df.where(lcoe_df["year"] <= 2021, lcoe_df.ffill())
    lcoe_df = lcoe_df.where(lcoe_df["year"] > 2021, lcoe_df.bfill())
    
    df = lcoe_df[["year", source]].set_index("year").rename(columns = {source: "electricity_price"})

    return df

