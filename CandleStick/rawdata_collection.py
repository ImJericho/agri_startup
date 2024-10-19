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

class AgriDataCollector:
    def __init__(self):
        self.url_template = ("https://agmarknet.gov.in/SearchCmmMkt.aspx?"
                             "Tx_Commodity=1&Tx_State=MP&Tx_District=12&Tx_Market=2440&"
                             "DateFrom={date_from}&DateTo={date_to}&"
                             "Fr_Date={date_from}&To_Date={date_to}&"
                             "Tx_Trend=0&Tx_CommodityHead={commodity}&"
                             "Tx_StateHead=Madhya+Pradesh&Tx_DistrictHead=Shajapur&Tx_MarketHead=Shajapur")

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

    # New method using requests
    def update_url(self, date_from, date_to, commodity):
        print("Updating URL")
        date_from_str = date_from.strftime('%d-%b-%Y')
        date_to_str = date_to.strftime('%d-%b-%Y')
        updated_url = self.url_template.format(date_from=date_from_str, date_to=date_to_str, commodity=commodity)
        return updated_url

    # Using requests 
    def collect_rawdata(self, date_from = datetime(2024, 1, 1), date_to = datetime(2024, 10, 20), commodity = "wheat"):
        print("Collecting raw data")
        url = self.update_url(date_from, date_to, commodity)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'cphBody_GridPriceData'})

        headers = [th.text.strip() for th in table.find_all('th')]
        data = [[td.text.strip() for td in tr.find_all('td')] for tr in table.find_all('tr')[1:]]

        print(data)
        df = pd.DataFrame(data, columns=headers)
        df['formatted_date'] = pd.to_datetime(df['Price Date'], format='%d %b %Y')
        df['formatted_date'] = df['formatted_date'].dt.strftime('%d-%m-%Y')

        csv_file_path = f'dataset/rawdata/{commodity}.csv'
        df.to_csv(csv_file_path, index=False)

if __name__ == "__main__":
    print("running the main function")
    collector = AgriDataCollector()
    # collector.old_method_using_selenium()

    new_from_date = datetime(2023, 1, 1)
    new_to_date = datetime(2024, 10, 20)
    commodity = "wheat"

    collector.collect_rawdata()
    # collector.collect_rawdata(new_from_date, new_to_date, commodity)