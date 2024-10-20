import logging
from pymongo import MongoClient
import constants
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class mongo_dao:
    def __init__(self, db_name = "CropsRealPrices"):
        client = MongoClient(constants.MONGO_URL)
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
        logging.info(f"Upserted document into {commodity} collection")
        return result

if __name__ == "__main__":
    commodities = pd.read_csv("dataset/metadata/commodity_of_intrest.csv")["Value"].tolist()
    commodities = ["Tomato"]
    dao = mongo_dao()
    for commodity in commodities:
        data = pd.read_csv(f"dataset/rawdata/{commodity}.csv")
        logging.info(f"Read data for {commodity}: {data.shape[0]} records")
        dao.insert_transactions(commodity, data)
        # dao.upsert_transactions(commodity, data)