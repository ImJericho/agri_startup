import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import csv
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgriDataCollector:
    def __init__(self):
        self.url_template = ("https://agmarknet.gov.in/SearchCmmMkt.aspx?"
                            "Tx_Commodity={commodity_no}&Tx_State={state_no}&Tx_District={district_no}&Tx_Market={market_no}&"
                             "DateFrom={date_from}&DateTo={date_to}&"
                             "Fr_Date={date_from}&To_Date={date_to}&"
                             "Tx_Trend=0&Tx_CommodityHead={commodity}&"
                             "Tx_StateHead={state}&Tx_DistrictHead={district}&Tx_MarketHead={market}")

    def _select_dropdown(self, driver, element_id, visible_text):
        element = driver.find_element(by=By.ID, value=element_id)
        select = Select(element)
        select.select_by_visible_text(visible_text)
        time.sleep(2)

    def old_method_using_selenium(self):
        driver = webdriver.Chrome()
        driver.get("https://agmarknet.gov.in/PriceAndArrivals/CommodityDailyStateWise.aspx")
        driver.implicitly_wait(5)

        self._select_dropdown(driver, "ddlArrivalPrice", "Price")
        self._select_dropdown(driver, "ddlCommodity", "Wheat")
        self._select_dropdown(driver, "ddlState", "Madhya Pradesh")
        self._select_dropdown(driver, "ddlDistrict", "Shajapur")
        self._select_dropdown(driver, "ddlMarket", "Shajapur")

        date_input = driver.find_element(By.ID, "txtDate")
        date_input.clear()
        date_input.send_keys("01-Jan-2023")
        time.sleep(10)
        date_input.send_keys(Keys.RETURN)
        time.sleep(40)

        go_button = driver.find_element(by=By.ID, value="btnGo")
        go_button.click()
        time.sleep(50)

        driver.quit()

    def parse_names(name):
        name = name.replace(' ', '+')
        return name

    def get_commodity_no(self, name):
        commodity = pd.read_csv('/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/commodity_list.csv')
        commodity_no = commodity[commodity['text'] == name]['value'].values[0]
        return commodity_no
    
    def get_state_no(self, name):
        state = pd.read_csv('/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/state_list.csv')
        state_no = state[state['text'] == name]['value'].values[0]
        return state_no
    
    def get_district_no(self, name):
        district = pd.read_csv('/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/district_list.csv')
        district_no = district[district['text'] == name]['value'].values[0]
        return district_no
    
    def get_market_no(self, name):
        market = pd.read_csv('/Users/vivek/Drive E/PROJECTS/agri_startup/CandleStick/dataset/metadata/market_list.csv')
        market_no = market[market['text'] == name]['value'].values[0]
        return market_no

    def update_url(self, date_from, date_to, commodity, state, district, market):
        logging.info("Updating URL with provided parameters")
        commodity_no = self.get_commodity_no(commodity)
        state_no = self.get_state_no(state)
        district_no = self.get_district_no(district)
        market_no = self.get_market_no(market)
        date_from_str = date_from.strftime('%d-%b-%Y')
        date_to_str = date_to.strftime('%d-%b-%Y')
        updated_url = self.url_template.format(date_from=date_from_str, date_to=date_to_str, commodity=commodity, state=state, district=district, market=market, commodity_no=commodity_no, state_no=state_no, district_no=district_no, market_no=market_no)
        logging.info(f"Updated URL: {updated_url}")
        return updated_url

    def collect_rawdata(self, date_from=datetime(2024, 1, 1), date_to=datetime(2024, 10, 20), commodity="Wheat", state="Madhya Pradesh", district="Shajapur", market="Shajapur"):
        logging.info("Starting raw data collection")
        url = self.update_url(date_from, date_to, commodity, state, district, market)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'cphBody_GridPriceData'})

        if not table:
            logging.warning("No data table found on the page")
            return pd.DataFrame()

        headers = [th.text.strip() for th in table.find_all('th')]
        data = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]

        if data == [['No Data Found']]:
            logging.info("No data found for the given parameters")
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=headers)
        df.rename(columns={'Sl no.': 'Sl No', 'Min Price (Rs./Quintal)': 'Min Price', 'Max Price (Rs./Quintal)': 'Max Price', 'Modal Price (Rs./Quintal)': 'Modal Price'}, inplace=True)
        df['formatted_date'] = pd.to_datetime(df['Price Date'], format='%d %b %Y')

        df['Min Price'] = pd.to_numeric(df['Min Price'], errors='coerce')
        df['Max Price'] = pd.to_numeric(df['Max Price'], errors='coerce')
        df['Modal Price'] = pd.to_numeric(df['Modal Price'], errors='coerce')
        df['Sl No'] = pd.to_numeric(df['Sl No'], errors='coerce')


        logging.info(f"Data collection for {commodity} completed successfully")
        return df

if __name__ == "__main__":
    logging.info("Running the main function")
    collector = AgriDataCollector()

    new_from_date = datetime(2023, 1, 1)
    new_to_date = datetime(2024, 10, 20)
    commodity = "Wheat"
    state = "Madhya Pradesh"
    district = "Shajapur"
    market = "Shajapur"

    collector.collect_rawdata(commodity=commodity)
