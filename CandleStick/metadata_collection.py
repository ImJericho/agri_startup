from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

class AgmarknetScraper:
    # Constructor
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)

    # Destructor
    def __del__(self):
        self.driver.quit()

    def get_options(self, element_id):
        element = self.driver.find_element(By.ID, element_id)
        select = Select(element)
        return [option.text for option in select.options]

    def save_to_csv(self, data_list, filename):
        df = pd.DataFrame(list(enumerate(data_list)), columns=['Index', 'Value'])
        df.to_csv(filename, index=False)

    def find_all_commodities(self):
        self.driver.get(self.url)
        commodity_list = self.get_options('ddlCommodity')
        self.save_to_csv(commodity_list, 'dataset/commodity_list.csv')
        return commodity_list

    def find_all_states(self):
        self.driver.get(self.url)
        state_list = self.get_options('ddlState')
        self.save_to_csv(state_list, 'dataset/state_list.csv')
        return state_list

    def find_all_districts(self, state_name):
        self.driver.get(self.url)
        state = self.driver.find_element(By.ID, 'ddlState')
        select = Select(state)
        select.select_by_visible_text(state_name)
        time.sleep(5)
        district_list = self.get_options('ddlDistrict')
        self.save_to_csv(district_list, 'dataset/district_list.csv')
        return district_list

    def find_all_markets(self, state_name, district_name):
        self.driver.get(self.url)
        state = self.driver.find_element(By.ID, 'ddlState')
        select = Select(state)
        select.select_by_visible_text(state_name)
        time.sleep(5)
        district = self.driver.find_element(By.ID, 'ddlDistrict')
        select = Select(district)
        select.select_by_visible_text(district_name)
        time.sleep(5)
        market_list = self.get_options('ddlMarket')
        self.save_to_csv(market_list, 'dataset/market_list.csv')
        return market_list

if __name__ == "__main__":
    scraper = AgmarknetScraper("https://agmarknet.gov.in/MarketWiseGraph/MarkGraphBoard.aspx")
    scraper.find_all_commodities()
    # scraper.find_all_states()
    # scraper.find_all_districts("Madhya Pradesh")
    # scraper.find_all_markets("Madhya Pradesh", "Shajapur")
