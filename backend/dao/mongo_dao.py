import logging
from pymongo import MongoClient
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MongoDao:
    def __init__(self, mongo_uri, db_name = "CropsRealPrices"):
        client = MongoClient(mongo_uri)
        self.db = client[db_name]
        logging.info(f"Connected to MongoDB database: {db_name}")
    
    def find_commodities(self, commodity, start_date, end_date):
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

    def get_commodity_list(self):
        return self.db.list_collection_names()
    
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