import pycountry
# Conversion for Efficiency
LHV = 33.33 #kWh/kg
LHV_N = 3 #kWh/Nm3
HHV = 39.33 #kWh/kg
def calc_new_efficiency(e, unit):
    if unit == 'HHV %':
        return e * LHV/HHV
    elif unit == 'LHV %':
        return e
    elif unit == "kWhe/kgH2":
        return LHV*100/e
    elif unit == 'kWh/Nm3H2':
        return LHV_N*100/e
    else:
        return 0


# Conversion for system size
def calc_new_sys_size(s, unit):
    if unit == 'MW':
        return s * 1000
    elif unit == 'kW':
        return s
    elif unit == "Nm3/h":
        return (s*LHV)/(3.6*1000)
    else:
        return 0

# Winsorizing the data
def winsorize(db, column, a, b):
    min, max = db[column].quantile([a, b])
    db = db[db[column].between(min, max)]
    return db

def get_country_name(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code).name
    except:
        return 'Unknown'

