from config.dev_config import DevConfig
from config.prod_config import ProdConfig

class Config:
    def __init__(self):
        self.development_config = DevConfig()
        self.production_config = ProdConfig()