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
url_template = ("https://agmarknet.gov.in/SearchCmmMkt.aspx?"
                "Tx_Commodity=1&Tx_State=MP&Tx_District=12&Tx_Market=2440&"
                "DateFrom={date_from}&DateTo={date_to}&"
                "Fr_Date={date_from}&To_Date={date_to}&"
                "Tx_Trend=0&Tx_CommodityHead=Wheat&"
                "Tx_StateHead=Madhya+Pradesh&Tx_DistrictHead=Shajapur&Tx_MarketHead=Shajapur")


def old_method_using_selenuim():
    driver = webdriver.Chrome()


    driver.get("https://agmarknet.gov.in/PriceAndArrivals/CommodityDailyStateWise.aspx")
    driver.implicitly_wait(5)


    # price_arrival = driver.find_elements(by=By.ID, value="ddlArrivalPrice")
    price_arrival = driver.find_element(by=By.ID, value ="ddlArrivalPrice")
    # comodity = driver.find_element(by=By.ID, value="ctl00$ddlCommodity")
    # state = driver.find_element(by=By.NAME, value="ctl00$ddlState")
    # district = driver.find_element(by=By.NAME, value="ctl00$ddlDistrict")
    # market = driver.find_element(by=By.NAME, value="ctl00$ddlMarket")
    # date_from = driver.find_element(by=By.NAME, value="ctl00$txtDate")
    # date_to = driver.find_element(by=By.NAME, value="ctl00$txtDateTo")
    # go_click = driver.find_element(by=By.NAME, value="market")

    # Create a Select object
    price_arrival = driver.find_element(by=By.ID, value ="ddlArrivalPrice")
    select = Select(price_arrival)
    select.select_by_visible_text("Price")
    time.sleep(2)


    comodity = driver.find_element(by=By.ID, value="ddlCommodity")
    select = Select(comodity)
    select.select_by_visible_text("Wheat")
    time.sleep(2)

    state = driver.find_element(by=By.ID, value="ddlState")
    select = Select(state)
    select.select_by_visible_text("Madhya Pradesh")
    time.sleep(5)

    district = driver.find_element(by=By.ID, value="ddlDistrict")
    select = Select(district)
    select.select_by_visible_text("Shajapur")
    time.sleep(5)

    market = driver.find_element(by=By.ID, value="ddlMarket")
    select = Select(market)
    select.select_by_visible_text("Shajapur")
    time.sleep(5)



    date_input = driver.find_element(By.ID, "txtDate")

    # Clear any existing text in the input field
    date_input.clear()

    # Type the desired date into the input field
    date_input.send_keys("01-Jan-2023")
    time.sleep(10)

    # Simulate pressing the Enter key
    date_input.send_keys(Keys.RETURN)

    time.sleep(40)




    # date_from_input = driver.find_element(By.ID, "txtDate")
    # date_from_input.click()
    # time.sleep(1)
    # date_from_to_select = driver.find_element(By.XPATH, "//div[@title='Monday, January 01, 2024']")
    # date_from_to_select.click()
    # time.sleep(2)

    # # date_from = driver.find_element(by=By.ID, value="txtDate")
    # # date_from.clear()
    # # date_from.send_keys("01-Jan-2024")
    # # time.sleep(5)

    # date_to_input = driver.find_element(By.ID, "txtDate")
    # date_to_input.click()
    # time.sleep(1)
    # date_to_to_select = driver.find_element(By.XPATH, "//div[@title='Monday, January 01, 2024']")
    # date_to_to_select.click()
    # time.sleep(2)

    # date_to = driver.find_element(by=By.ID, value="txtDateTo")
    # date_from.clear()
    # date_from.send_keys("01-Oct-2024")
    # time.sleep(5)

    time.sleep(2)
    go_button = driver.find_element(by=By.ID, value="btnGo")
    go_button.click()
    time.sleep(2)


    time.sleep(50)






    # text_box = driver.find_element(by=By.NAME, value="my-text")
    # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    # text_box.send_keys("Selenium")
    # submit_button.click()

    # message = driver.find_element(by=By.ID, value="message")
    # text = message.text

    driver.quit()
# Function to change dates in the URL
def update_url_with_dates(date_from, date_to):
    # Convert input dates to the required format 'dd-MMM-yyyy'
    date_from_str = date_from.strftime('%d-%b-%Y')
    date_to_str = date_to.strftime('%d-%b-%Y')
    # Substitute the dates in the URL template
    updated_url = url_template.format(date_from=date_from_str, date_to=date_to_str)
    return updated_url

def update_url():
    # Example usage - dynamically setting the dates
    new_from_date = datetime(2023, 1, 1)  # Change to your desired start date
    new_to_date = datetime(2024, 10, 20)   # Change to your desired end date

    # Get the updated URL
    updated_url = update_url_with_dates(new_from_date, new_to_date)

    return updated_url


# if __name__ == '__main__':
def using_selenium():
    url = update_url()
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    table = driver.find_element(By.XPATH, '//table[@id="cphBody_GridPriceData"]')  # Replace with the actual table ID

    # Extract header and data rows
    header_row = table.find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')
    header = [th.text.strip() for th in header_row]

    data_rows = table.find_elements(By.TAG_NAME, 'tr')[1:]  # Skip the header row
    data = []
    for row in data_rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

    # Create a Pandas DataFrame from the extracted data
    df = pd.DataFrame(data, columns=header)

    # Save the DataFrame as a CSV file
    df.to_csv('price_data.csv', index=False)

    driver.quit()



def using_request():
    url = update_url()
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table in the parsed HTML
    table = soup.find('table', {'id': 'cphBody_GridPriceData'})

    # Extract table headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())

    # Extract table rows
    data = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        data.append(row)

    # Create a DataFrame from the extracted data

    df = pd.DataFrame(data, columns=headers)

    df['formatted_date'] = pd.to_datetime(df['Price Date'], format='%d %b %Y')
    df['formatted_date'] = df['formatted_date'].dt.strftime('%d-%m-%Y')
    

    # Save the DataFrame to a CSV file
    csv_file_path = 'dataset/raw_data.csv'
    df.to_csv(csv_file_path, index=False)


if __name__ == "__main__":
    # using_selenium()
    using_request()