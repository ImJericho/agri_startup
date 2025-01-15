from dao.mongo_dao import MongoDao
from config.config import Config
from routes import api
from flask import Flask
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
config = Config().development_config
app.env = config.ENV
app.mongo_dao = MongoDao(config.MONGO_URI)

app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)