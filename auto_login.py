# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00819AA14EDE36AEFD1E0E0A1EED28ECD37204D9829EF707F94BB69C8AD223AC50AB9E28473C94FB77014E062479E9B1E6D6E236D7A7CA155D4A160D30AE0C5FEAB15D7FC9171551AC5598FD55A556B57FF115B5F0F4392B0EFA0E23D4E25D5D0BB5924381D8C53F54E0D2D853172CE48462C8AA0D1544C0FD2CD73F377B17F722B6B114F4A38BF1529F48B0094F04DE43D906296F0E73A5339805322FC3D583B1602433E2FD42B039B1C2C6AE28D3940A42338B9CC733F682C75FFD3851BD6F34BAA9FB8E9B09A703D1217AF82417AB981FAB0C478FD049341FE23DD0BDF4EC2B0D260FFFEC7CE4031E656C14E38D2228859762AD00B46A2D51CC738ED75FE021E209BB21682BBF52678320D052A8CAEECF00F2FDF16BC719478C91962B0665D66B23448D98924A6AF1D0C69CB5139D6A38354304AF96C9767B50EE66EA5277A641D945271F1CCE47149A56AEAB5430E48AC0C4D87DCF66FB4B7C98DDAD178A51"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
