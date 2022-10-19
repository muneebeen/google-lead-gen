from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import gspread
import json


def configure_driver(options_set):
    d = webdriver.Chrome(options=options_set)
    return d


def configure_webdriver_options():
    o = webdriver.ChromeOptions()
    o.add_experimental_option("excludeSwitches", ["enable-automation"])
    o.add_experimental_option('useAutomationExtension', False)
    o.add_argument("--disable-blink-features=AutomationControlled")
    o.add_argument("--window-size=1880,1300")
    o.add_argument("--disable-notifications")
    # o.headless = True
    return o


def file_creator(filename, data):
    info_json = json.dumps(data)
    with open(filename, "w") as outfile:
        outfile.write(info_json)


if __name__ == '__main__':
    sheet_name = 'Search Queries'
    gc = gspread.service_account(filename="Enter File Name Here")
    sh = gc.open(sheet_name).get_worksheet(0)

    # Getting values from first column
    queries_list = sh.col_values(1)

    # configuring options
    options = configure_webdriver_options()

    # configuring driver
    driver = configure_driver(options)

    # selectors
    google_search_input = "input[title='Search']"
    google_search_btn = "input[value='Google Search']"

    for query in queries_list:
        all_data = []
        driver.get('https://www.google.com')
        sleep(3)
        driver.find_element(By.CSS_SELECTOR, google_search_input).send_keys(query)
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, google_search_btn).click()
        sleep(2)
        if len(driver.find_elements(By.XPATH, "//*[text()='More places']")) < 1:
            continue
        driver.find_element(By.XPATH, "//*[text()='More places']").click()
        sleep(2)
        next_btn = driver.find_element(By.XPATH, "//*[text()='Next']")
        is_next_btn = next_btn.is_displayed()
        n = 2
        while is_next_btn:
            items = driver.find_elements(By.CSS_SELECTOR, "[jscontroller='AtSb']")
            sleep(2)
            for i in range(len(items)):
                items = driver.find_elements(By.CSS_SELECTOR, "[jscontroller='AtSb']")
                sleep(2)
                items[i].click()
                sleep(2)
                name = website = reviews = ratings = address = phone = ""
                if len(driver.find_elements(By.CSS_SELECTOR, '[data-attrid="title"]')) > 0:
                    name = driver.find_element(By.CSS_SELECTOR, '[data-attrid="title"]').text
                if len(driver.find_elements(By.CSS_SELECTOR, '.QqG1Sd:nth-child(1) > a')) > 0:
                    value = driver.find_element(By.CSS_SELECTOR, '.QqG1Sd:nth-child(1) > a').get_attribute('href')
                    if "google.com" not in value:
                        website = value
                if len(driver.find_elements(By.CSS_SELECTOR, ".hqzQac a > span")) > 0:
                    reviews = driver.find_element(By.CSS_SELECTOR, ".hqzQac a > span").text
                if len(driver.find_elements(By.CSS_SELECTOR, ".Aq14fc")) > 0:
                    ratings = driver.find_element(By.CSS_SELECTOR, ".Aq14fc").text
                if len(driver.find_elements(By.CSS_SELECTOR, '.SALvLe .LrzXr')) > 0:
                    address = driver.find_element(By.CSS_SELECTOR, '.SALvLe .LrzXr').text
                if len(driver.find_elements(By.CSS_SELECTOR, '.kno-fv >  a > span > span')) > 0:
                    phone = driver.find_element(By.CSS_SELECTOR, '.kno-fv >  a > span > span').text

                item_data = {
                    'Name': name,
                    'Website': website,
                    'Reviews': reviews,
                    'Rating': ratings,
                    'Address': address,
                    'Phone': phone,
                }
                all_data.append(item_data)

            n += 1
            if len(driver.find_elements(By.XPATH, "//*[text()='Next']")) > 0:
                next_btn = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[text()='Next']")))
                is_next_btn = next_btn.is_displayed()
                next_btn.click()
                sleep(2)
            else:
                file_creator(query, all_data)
                is_next_btn = False
                break







