from pymongo import MongoClient
import common.constants as constants
import config



def get_mongo_client():
    return MongoDBDriver().client

class MongoDBDriver:
    def __init__(self): 
        self.client = MongoClient(config.config().get_mongo_url())
        self.db = None

    def connect_to_database(self, db_name="AgriStartup"):
        self.db = self.client[db_name]

    def connect_to_collection(self, collection_name):
        return self.db[collection_name]

    # def insert_one(self, collection_name, document):
    #     collection = self.db[collection_name]
    #     result = collection.insert_one(document)
    #     return result.inserted_id

    # def find_one(self, collection_name, query):
    #     collection = self.db[collection_name]
    #     document = collection.find_one(query)
    #     return document

    # def find_many(self, collection_name, query):
    #     collection = self.db[collection_name]
    #     documents = collection.find(query)
    #     return list(documents)

    # def update_one(self, collection_name, query, update):
    #     collection = self.db[collection_name]
    #     result = collection.update_one(query, update)
    #     return result.modified_count

    # def delete_one(self, collection_name, query):
    #     collection = self.db[collection_name]
    #     result = collection.delete_one(query)
    #     return result.deleted_count



if __name__ == "__main__":
    print("mongo")

    # Example usage:
    # connection_string = const.MONGO_URL
    # mongo_driver = MongoDBDriver(connection_string)
    # mongo_db = mongo_driver.connect_to_database("your_database_name")
    # mongo_driver.insert_one("your_collection_name", {"key": "value"})


    # client = MongoClient(const.MONGO_URL, server_api=ServerApi('1'))
    # mongodb = client["vivek_db"]
    # collection = mongodb["hell_and_heven"]