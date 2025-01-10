import data_collection.rawdata_collection as rdc
from datetime import datetime, timedelta, timezone
import pandas as pd
import dao.mongo_dao as mongo_dao
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.warning(f"File not found for {commodity}. Creating a new file.")
        existing_df = pd.DataFrame(columns=["Sl no.", "District Name", "Market Name", "Commodity", "Variety", "Grade", 
                                            "Min Price (Rs./Quintal)", "Max Price (Rs./Quintal)", 
                                            "Modal Price (Rs./Quintal)", "Price Date", "formatted_date"])
    new_df = pd.DataFrame(new_data)
    if new_data.empty:
        existing_df.to_csv(file_path, index=False)
        logging.info("No new data provided for upsert. Operation skipped.")
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
    logging.info("Data upserted on Local successfully!")

def upsert_data_atlas(md, commodity, new_data):
    md.upsert_transactions(commodity, new_data)
    logging.info("Data upserted on Atlas successfully!")

def find_all_commodities_of_intrest():
    df = pd.read_csv("/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/commodity_of_intrest.csv")
    commodities = df["Name"].tolist()
    logging.info(f"Commodities of interest: {commodities}")
    return commodities

def process_commodity_manual(commodity, from_date, to_date, market_list, mongo_client, collector):
    for _, market in market_list.iterrows():
        data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
        upsert_data_atlas(mongo_client, commodity, data)
        logging.info(f"Data collected for {market['text']}, and of size {data.shape}")

def process_commodity(commodity, cron, market_list, mongo_client):
    collector = rdc.AgriDataCollector()
    from_date = cron.loc[cron['name'] == "Wheat", 'last scrap date'].values[0]
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.now()

    print(f"===called for {commodity}")
    for _, market in market_list.iterrows():
        data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
        upsert_data_atlas(mongo_client, commodity, data)
        logging.info(f"Data collected for {market['text']}, and of size {data.shape}")

    cron.loc[cron['name'] == commodity, 'last scrap date'] = to_date.strftime('%Y-%m-%d')
    cron.to_csv("cron.csv", index=False)



if __name__ == "__main__":

    market_list = pd.read_csv("/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/market_list.csv")
    mongo_client = mongo_dao.mongo_dao()

    cron_job = pd.read_csv("/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/cron.csv")
    print(cron_job.head())

    commodities = find_all_commodities_of_intrest()
    new_commodities = []
    for commodity in commodities:
        if cron_job.loc[cron_job['name'] == commodity, 'active'].values[0] == 1:
            new_commodities.append(commodity)


    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_commodity, commodity, cron_job, market_list, mongo_client) for commodity in new_commodities]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing commodity: {e}")
