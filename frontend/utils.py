import pandas as pd

def get_commodity_list():
    commodity = pd.read_csv("frontend/data/metadata/commodity_of_intrest.csv")
    commodity_list = []
    for i in range(len(commodity)):
        commodity_list.append(commodity['Name'][i])
        # commodity_list.append(f"{commodity['Name'][i]}+'({commodity['display_name'][i]}")
    print(commodity_list)
    return commodity_list