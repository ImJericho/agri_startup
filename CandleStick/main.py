import rawdata_collection as rdc
from datetime import datetime, timedelta, timezone
import pandas as pd
import mongo_dao

class TimeDataHandler:
    def __init__(self):
        self.IST = timezone(timedelta(hours=5, minutes=30))

    def date_range_for_past_x_days(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x)
        return to_date, from_date

    def date_range_for_past_x_months(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*30)
        return to_date, from_date

    def date_range_for_past_x_years(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*365)
        return to_date, from_date

    def date_range_for_past_x_weeks(self, x):
        to_date = datetime.now(self.IST).date()
        from_date = to_date - timedelta(days=x*7)
        return to_date, from_date

def upsert_data_locally(commodity, new_data):
    file_path = f'dataset/rawdata/{commodity}.csv'
    try:
        # Load the existing data from CSV
        existing_df = pd.read_csv(file_path)
    except FileNotFoundError:
        # If file doesn't exist, create an empty DataFrame with the required columns
        print(f"File not found for {commodity}. Creating a new file.")
        existing_df = pd.DataFrame(columns=["Sl no.", "District Name", "Market Name", "Commodity", "Variety", "Grade", 
                                            "Min Price (Rs./Quintal)", "Max Price (Rs./Quintal)", 
                                            "Modal Price (Rs./Quintal)", "Price Date", "formatted_date"])
    new_df = pd.DataFrame(new_data)
    if new_data.empty:
        existing_df.to_csv(file_path, index=False)
        print("No new data provided for upsert. Operation skipped.")
        return
    # Ensure that both DataFrames have 'formatted_date' as a string type
    existing_df['formatted_date'] = existing_df['formatted_date'].astype(str)
    new_df['formatted_date'] = new_df['formatted_date'].astype(str)
    # Merge and update data by 'formatted_date' index
    updated_df = pd.concat([existing_df.set_index('formatted_date'), new_df.set_index('formatted_date')], axis=0)
    # Keep the latest entry for each 'formatted_date' (i.e., remove duplicates)
    updated_df = updated_df.groupby(updated_df.index).last().reset_index()
    # Save the updated data back to the CSV
    updated_df.to_csv(file_path, index=False)
    print("Data upserted on Local successfully!")


def upsert_data_atlas(md, commodity, new_data):
    md.upsert_transactions(commodity, new_data)
    print("Data upserted on Atals successfully!")

def find_all_commodities_of_intrest():
    df = pd.read_csv("dataset/metadata/commodity_of_intrest.csv")
    commodities = df["Value"].tolist()
    print("commodities of interest:", commodities)
    return commodities


if __name__ == "__main__":
    collector = rdc.AgriDataCollector()
    new_from_date = datetime(2023, 1, 1)
    new_to_date = datetime(2024, 10, 18)

    commodities = find_all_commodities_of_intrest()
    # commodities = ["Potato"]

    mongo_client = mongo_dao.mongo_dao()

    for commodity in commodities:
        print(f"Collecting data for {commodity}")
        new_data = collector.collect_rawdata(new_from_date, new_to_date, commodity)
        # upsert_data_locally(commodity, new_data)
        upsert_data_atlas(mongo_client, commodity, new_data)
        print(f"Data for {commodity} collected successfully")
