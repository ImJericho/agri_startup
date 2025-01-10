from datetime import datetime
import pandas as pd
import logging
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
MONGO_URL = os.getenv("MONGO_URL")

class mongo_dao:
    def __init__(self, db_name = "CropsRealPrices"):
        client = MongoClient(MONGO_URL)
        self.db = client[db_name]
        logging.info(f"Connected to MongoDB database: {db_name}")
    
    def insert_transactions(self, commodity, documents):
        data = documents.to_dict('records') 
        collection = self.db[commodity]
        if len(data) == 0:
            logging.info(f"No documents to insert for {commodity}")
            return
        elif len(data) == 1:
            result = collection.insert_one(data[0])
            logging.info(f"Inserted one document into {commodity} collection")
        else:
            result = collection.insert_many(data)
            logging.info(f"Inserted {len(data)} documents into {commodity} collection")
        return 

    def upsert_transactions(self, commodity, documents):
        data = documents.to_dict('records')
        collection = self.db[commodity]
        result = None
        for doc in data:
            query = {
                "District Name": doc["District Name"],
                "Market Name": doc["Market Name"],
                "formatted_date": doc["formatted_date"],
            }
            update = {
                "$set": doc
            }
            result = collection.update_one(query, update, upsert=True)
        # logging.info(f"Upserted document into {commodity} collection")
        return result


class AgriDataCollector:
    def __init__(self):
        self.url_template = ("https://agmarknet.gov.in/SearchCmmMkt.aspx?"
                            "Tx_Commodity={commodity_no}&Tx_State={state_no}&Tx_District={district_no}&Tx_Market={market_no}&"
                             "DateFrom={date_from}&DateTo={date_to}&"
                             "Fr_Date={date_from}&To_Date={date_to}&"
                             "Tx_Trend=0&Tx_CommodityHead={commodity}&"
                             "Tx_StateHead={state}&Tx_DistrictHead={district}&Tx_MarketHead={market}")

    def parse_names(name):
        name = name.replace(' ', '+')
        return name

    def get_commodity_no(self, name):
        commodity = pd.read_csv('frontend/data/metadata/commodity_list.csv')
        commodity_no = commodity[commodity['text'] == name]['value'].values[0]
        return commodity_no
    
    def get_state_no(self, name):
        state = pd.read_csv('frontend/data/metadata/state_list.csv')
        state_no = state[state['text'] == name]['value'].values[0]
        return state_no
    
    def get_district_no(self, name):
        district = pd.read_csv('frontend/data/metadata/district_list.csv')
        district_no = district[district['text'] == name]['value'].values[0]
        return district_no
    
    def get_market_no(self, name):
        market = pd.read_csv('frontend/data/metadata/market_list.csv')
        market_no = market[market['text'] == name]['value'].values[0]
        return market_no

    def update_url(self, date_from, date_to, commodity, state, district, market):
        # logging.info("Updating URL with provided parameters")
        commodity_no = self.get_commodity_no(commodity)
        state_no = self.get_state_no(state)
        district_no = self.get_district_no(district)
        market_no = self.get_market_no(market)
        date_from_str = date_from.strftime('%d-%b-%Y')
        date_to_str = date_to.strftime('%d-%b-%Y')
        updated_url = self.url_template.format(date_from=date_from_str, date_to=date_to_str, commodity=commodity, state=state, district=district, market=market, commodity_no=commodity_no, state_no=state_no, district_no=district_no, market_no=market_no)
        # logging.info(f"Updated URL: {updated_url}")
        return updated_url

    def collect_rawdata(self, date_from=datetime(2025, 1, 1), date_to=datetime(2024, 10, 20), commodity="Wheat", state="Madhya Pradesh", district="Shajapur", market="Shajapur"):
        url = self.update_url(date_from, date_to, commodity, state, district, market)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'cphBody_GridPriceData'})

        if not table:
            logging.warning(f"No data found on the page::: {url}")
            return pd.DataFrame()

        headers = [th.text.strip() for th in table.find_all('th')]
        data = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]

        if data == [['No Data Found']]:
            logging.warning(f"No data found on the page::: {url}")
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=headers)
        df.rename(columns={'Sl no.': 'Sl No', 'Min Price (Rs./Quintal)': 'Min Price', 'Max Price (Rs./Quintal)': 'Max Price', 'Modal Price (Rs./Quintal)': 'Modal Price'}, inplace=True)
        df['formatted_date'] = pd.to_datetime(df['Price Date'], format='%d %b %Y')

        df['Min Price'] = pd.to_numeric(df['Min Price'], errors='coerce')
        df['Max Price'] = pd.to_numeric(df['Max Price'], errors='coerce')
        df['Modal Price'] = pd.to_numeric(df['Modal Price'], errors='coerce')
        df['Sl No'] = pd.to_numeric(df['Sl No'], errors='coerce')

        logging.info(f"Data collection for {commodity} and {market} completed successfully")
        return df

def find_all_commodities_of_interest():
    df = pd.read_csv("frontend/data/metadata/commodity_of_intrest.csv")
    commodities = df["Name"].tolist()
    logging.info(f"Commodities of interest: {commodities}")
    return commodities

def upsert_data_atlas(md, commodity, new_data):
    md.upsert_transactions(commodity, new_data)


def process_commodity(commodity, cron, market_list):
    mongo_client = mongo_dao()
    collector = AgriDataCollector()

    if commodity in cron['name'].values:
        from_date = cron.loc[cron['name'] == commodity, 'last_scrap_date'].values[0]
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.now()
    else:
        from_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
        to_date = datetime.now()
        new_row = pd.DataFrame([{'sno': len(cron)+1, 'name': commodity, 'type': 'commodity', 'first_scrap_date': from_date, 'active': 1}])
        cron = pd.concat([cron, new_row], ignore_index=True)
    logging.info(f"===called for {commodity}, {from_date}, {to_date}")

    for _, market in market_list.iterrows():
        data = collector.collect_rawdata(from_date, to_date, commodity, market['state'], market['district'], market['text'])
        upsert_data_atlas(mongo_client, commodity, data)
        logging.info(f"Data uploaded for {commodity} for {market['text']}, and of size {data.shape}")

    # cron.loc[cron['name'] == commodity, 'last_scrap_date'] = to_date.strftime('%Y-%m-%d')
    # cron = cron.loc[:, ~cron.columns.str.contains('^Unnamed')]
    # cron.to_csv("frontend/cron.csv", index=False)

    logging.info(f"===Process Completed for {commodity}")
    return True
