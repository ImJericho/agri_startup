
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
