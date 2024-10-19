import rawdata_collection as rdc
from datetime import datetime, timedelta, timezone
import pandas as pd


def find_all_commodities_of_intrest():
    df = pd.read_csv("dataset/metadata/commodity_of_intrest.csv")
    commodities = df["Value"].tolist()
    print("commodities of intrest :", commodities)
    commodities = [commodity.lower() for commodity in commodities]
    return commodities

def date_range_for_past_x_days(x):
    IST = timezone(timedelta(hours=5, minutes=30))
    to_date = datetime.now(IST).date()
    x_days = x  # For example, 10 days
    from_date = to_date - timedelta(days=x_days)

    return to_date, from_date

def date_range_for_past_x_months(x):
    IST = timezone(timedelta(hours=5, minutes=30))
    to_date = datetime.now(IST).date()
    x_months = x  # For example, 3 months
    from_date = to_date - timedelta(days=x_months*30)

    return to_date, from_date

if __name__ == "__main__":
    collector = rdc.AgriDataCollector()
    new_from_date = datetime(2024, 1, 1)
    new_to_date = datetime(2024, 10, 20)

    commodities = find_all_commodities_of_intrest()

    for commodity in commodities:
        print(f"Collecting data for {commodity}")
        try:
            existing_df = pd.read_csv(f'dataset/rawdata/{commodity}.csv')
        except FileNotFoundError:
            # If the file doesn't exist, create an empty DataFrame with the required columns(Sl no.,District Name,Market Name,Commodity,Variety,Grade,Min Price (Rs./Quintal),Max Price (Rs./Quintal),Modal Price (Rs./Quintal),Price Date,formatted_date)
            print(f"File not found for {commodity}. Creating a new file")
            existing_df = pd.DataFrame(columns=["Sl no.", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min Price (Rs./Quintal)", "Max Price (Rs./Quintal)", "Modal Price (Rs./Quintal)", "Price Date", "formatted_date"])
        new_data = collector.collect_rawdata(new_from_date, new_to_date, commodity)
        new_df = pd.DataFrame(new_data)
        updated_df = pd.concat([existing_df.set_index('formatted_date'), new_df.set_index('formatted_date')], axis=0)
        updated_df = updated_df.groupby(updated_df.index).last().reset_index()
        updated_df.to_csv(f'dataset/rawdata/{commodity}.csv', index=False)

        print(f"Data for {commodity} collected successfully")

    collector.collect_rawdata()