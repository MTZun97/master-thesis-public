import pandas as pd
ng_price = pd.DataFrame.from_dict({"Countries": ["Australia", "Spain", "Germany", "China", "Netherlands", "Japan",
                          "Canada", "United States", "United Kingdom","Sweden"],
            "ng_price": [0.07, 0.17, 0.21, 0.01 ,0.41, 0.11, 0.03, 0.05, 0.1, 0.24]}).set_index("Countries") #China assumption
ng_cv = pd.DataFrame.from_dict({"Countries": ["Australia", "Spain", "Germany", "China", "Netherlands", "Japan",
                          "Canada", "United States", "United Kingdom","Sweden"],
            "ng_cv": [11.055, 11.867, 9.769, 11.5, 9.776, 12.793, 10.341, 10.629, 9.769, 11.5]}).set_index("Countries") #China,Sweden assumption

grey_H2 = pd.concat([ng_price,ng_cv], axis = 1)
grey_H2["ng_price_m3"] = grey_H2["ng_price"]*grey_H2["ng_cv"]
grey_H2["grey_H2_cost"] = [(5.08 * i) + 0.3918 for i in grey_H2["ng_price_m3"]]
