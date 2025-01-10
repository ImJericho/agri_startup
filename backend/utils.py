import time
from datetime import datetime, timedelta, timezone
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def find_all_commodities_of_interest():
    df = pd.read_csv("backend/data/metadata/commodity_of_intrest.csv")
    commodities = df["Name"].tolist()
    logging.info(f"Commodities of interest: {commodities}")
    return commodities

def upsert_data_atlas(md, commodity, new_data):
    md.upsert_transactions(commodity, new_data)
    # logging.info(f"Data upserted on Atlas successfully for {commodity}!")

def process_commodity_manual(commodity, from_date, to_date, market_list, mongo_client, collector):
    for _, market in market_list.iterrows():
        data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
        upsert_data_atlas(mongo_client, commodity, data)
        logging.info(f"Data collected for {market['text']}, and of size {data.shape}")

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