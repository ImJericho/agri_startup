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
        return [{"value":option.get_attribute('value'), "text":option.text} for option in select.options]

    def save_to_csv(self, data_list, filename):
        df = pd.DataFrame(data_list)
        df.to_csv(filename, index=False)

    def find_all_commodities(self, do_save=False):
        self.driver.get(self.url)
        commodity_list = self.get_options('ddlCommodity')
        for commodity in commodity_list:
            print(commodity)
        if do_save:
            self.save_to_csv(commodity_list, '/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/commodity_list.csv')
        return commodity_list

    def find_all_states(self, do_save=False):
        self.driver.get(self.url)
        state_list = self.get_options('ddlState')
        for state in state_list:
            print(state)

        if do_save:
            self.save_to_csv(state_list, '/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/state_list.csv')
        return state_list

    def find_all_districts(self, state_name, do_save=False):
        self.driver.get(self.url)
        state = self.driver.find_element(By.ID, 'ddlState')
        select = Select(state)
        select.select_by_visible_text(state_name)
        time.sleep(5)
        district_list = self.get_options('ddlDistrict')
        for district in district_list:
            district['state'] = state_name
            print(district)

        if do_save:
            self.save_to_csv(district_list, '/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/district_list.csv')
        return district_list

    def find_all_markets(self, state_name, district_name, do_save=False):
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
        for market in market_list:
            market['state'] = state_name
            market['district'] = district_name
            print(market)
        
        if do_save:
            self.save_to_csv(market_list, '/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/market_list.csv')
        return market_list

if __name__ == "__main__":
    scraper = AgmarknetScraper("https://agmarknet.gov.in/MarketWiseGraph/MarkGraphBoard.aspx")
    # scraper.find_all_commodities()
    # scraper.find_all_states()
    # scraper.find_all_districts("Madhya Pradesh")
    # scraper.find_all_markets("Madhya Pradesh", "Shajapur")

    district_of_interest = ["Shajapur", "Agar Malwa", "Dewas", "Indore", "Neemuch", "Rajgarh", "Ujjain"]

    main_market_list = []
    for district in district_of_interest:
        market_list = scraper.find_all_markets("Madhya Pradesh", district)
        market_list = market_list[1:]
        main_market_list.extend(market_list)
        print(f"District: {district}, Markets: {len(market_list)}")
        time.sleep(5)

    df = pd.DataFrame(main_market_list)
    df.to_csv('dataset/metadata/market_list.csv', index=False)
