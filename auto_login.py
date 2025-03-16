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
    browser.add_cookie({"name": "MUSIC_U", "value": "003F3493833FCBDF909E12A8E02ADA1734E0A0158946B1DD5BADFC8943EA045AA0E980D829F7E5C1C2A624E2D1D6883FA125AB46F83C1F76C22A2C49C0039845A16CA5DA69C8EC15A49F8D82ED1E67FBAEF0C52CDB24537D18A28684A8CEF8462EE8DAB19E253ECA97A1CC6241562F4D516868AF2383A6FDDD68D07EB601C92A1E057411827059E2CA99396529B32AB1D9B7C3C4436DD13745DF74BCFF58000AD8F6EC0F4181595ECF1D2FEC052F7DAB854FB3C250E2BCDCC533F6E2C70F90973C759BF5246456D478366D048B25151BD6DE45F30E2C359C03ACF5B012A9CCB139735A2D14F6324585325793DE92E27D4AB96D72093FFEFB3723F1FAE004C92979AC6884ADF0F1B6B0EF1FFF4EC35D5A6F093F543739D7D9070F0CD5CF42FAD3797ED16EC9C1359B86D647EB21760460CE718F0AB4FC1A175FB873F70173799D3C1654778056BB0F1A18068A2AC3ADC6DB090305F1A3701F8862CF31F053EBDE9B"})
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
