import common.constants as constants 


class config:
    def __init__(self):
        self.mongo_url = constants.MONGO_URL
        self.config = {
            "name": "config",
            "version": "0.1",
            "debug": True,
            "port": 8000,
            "host": "",
        }
    def get_config(self):
        return self.config
    
    def get_mongo_url(self):
        return self.mongo_url
    