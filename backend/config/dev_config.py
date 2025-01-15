import os
from dotenv import load_dotenv
load_dotenv()


class DevConfig:
    def __init__(self):
        self.ENV = "devlopemnt"
        self.DEBUG = True
        self.HOST = "0.0.0.0"
        self.PORT = 3000
        self.MONGO_URI = os.getenv("MONGO_URL")

