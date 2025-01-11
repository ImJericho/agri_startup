import logging
from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MONGO_URL = os.getenv("MONGO_URL")

class mongo_dao:
    def __init__(self, db_name = "CropsRealPrices"):
        client = MongoClient(MONGO_URL)
        self.db = client[db_name]
        logging.info(f"Connected to MongoDB database: {db_name}")
    
    def find_commodities(self, commodity, district, market, start_date, end_date):
        collection = self.db[commodity]
        query = {
            "District Name": district,
            "Market Name": market,
            "formatted_date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        logging.info(f"Finding documents in {commodity} collection with query: {query}")
        documents = collection.find(query)
        return documents
    
    def find_commodities(self, commodity, start_date, end_date):
        collection = self.db[commodity]
        query = {
            'formatted_date': {
                '$gte': start_date,
                '$lte': end_date
            }
        }

        logging.info(f"Finding documents in {commodity} collection with query: {query}")
        documents = collection.find(query)
        return documents
    
    def find_commodities_prices(self, commodity, start_date, end_date):
        collection = self.db[commodity]
        query = {
            'formatted_date': {
            '$gte': start_date,
            '$lte': end_date
            }
        }
        projection = {
            'Modal Price': 1,
            'formatted_date': 1,
            'Market Name': 1,
            '_id': 0
        }
        logging.info(f"Finding documents in {commodity} collection with query: {query} and projection: {projection}")
        documents = collection.find(query, projection)
        return documents
    
    # def find_commodities(self, commodity):
    #     collection = self.db[commodity]
    #     query = {
    #     }

    #     logging.info(f"Finding documents in {commodity} collection with query: {query}")
    #     documents = collection.find(query)
    #     return documents

    def get_commodity_list(self):
        return self.db.list_collection_names()

if __name__ == "__main__":
    commodities = pd.read_csv("dataset/metadata/commodity_of_intrest.csv")["Value"].tolist()
    commodities = ["Tomato"]
    dao = mongo_dao()
    for commodity in commodities:
        data = pd.read_csv(f"dataset/rawdata/{commodity}.csv")
        logging.info(f"Read data for {commodity}: {data.shape[0]} records")
        dao.insert_transactions(commodity, data)
        # dao.upsert_transactions(commodity, data)