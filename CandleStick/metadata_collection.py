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



# Original URL string with placeholder dates

common_url = "https://agmarknet.gov.in/MarketWiseGraph/MarkGraphBoard.aspx"



def find_all_commodities():
    url = common_url
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    commoditie = driver.find_element(By.ID, 'ddlCommodity')
    select = Select(commoditie)
    commodity_list = [option.text for option in select.options]
    for commodity in commodity_list:
        print(commodity)
    driver.quit()

    df = pd.DataFrame(list(enumerate(commodity_list)), columns=['Index', 'Value'])
    df.to_csv('dataset/commodity_list.csv', index=False)

    return commodity_list

def find_all_states():
    url = common_url
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    state = driver.find_element(By.ID, 'ddlState')
    select = Select(state)
    state_list = [option.text for option in select.options]
    for district in state_list:
        print(district)
    driver.quit()

    df = pd.DataFrame(list(enumerate(state_list)), columns=['Index', 'Value'])
    df.to_csv('dataset/state_list.csv', index=False)

    return state_list

def find_all_district(state_name):
    url = common_url
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    state = driver.find_element(by=By.ID, value="ddlState")
    select = Select(state)
    select.select_by_visible_text(state_name)
    time.sleep(5)

    district = driver.find_element(By.ID, 'ddlDistrict')
    select = Select(district)
    district_list = [option.text for option in select.options]
    for district in district_list:
        print(district)
    driver.quit()


    df = pd.DataFrame(list(enumerate(district_list)), columns=['Index', 'Value'])
    df.to_csv('dataset/district_list.csv', index=False)

    return district_list 

def find_all_markets(state_name, district_name):
    url = common_url
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    state = driver.find_element(by=By.ID, value="ddlState")
    select = Select(state)
    select.select_by_visible_text(state_name)
    time.sleep(5)

    district = driver.find_element(By.ID, 'ddlDistrict')
    select = Select(district)
    select.select_by_visible_text(district_name)
    time.sleep(5)


    market = driver.find_element(By.ID, 'ddlMarket')
    select = Select(market)
    market_list = [option.text for option in select.options]
    for market in market_list:
        print(market)
    driver.quit()
    df = pd.DataFrame(list(enumerate(market_list)), columns=['Index', 'Value'])
    df.to_csv('dataset/market_list.csv', index=False)
    return market_list



if __name__ == "__main__":
    # using_selenium()
    # using_request()



    find_all_commodities()
    # find_all_states()
    # find_all_district("Madhya Pradesh")
    # find_all_markets("Madhya Pradesh", "Shajapur")
