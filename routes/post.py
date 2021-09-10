import os
import json
from flask import Blueprint
from selenium.webdriver.chrome.options import Options
from selenium import webdriver



post = Blueprint('post', __name__)

def set_chrome_options() -> None:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

@post.route('/st') 
def post_stocktwits():
    print(os.getenv('CHROME_DRIVER_URL'))
    driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    driver.get("http://www.stocktwits.com")
    driver.implicitly_wait(10)
    # login
    python_button = driver.find_elements_by_xpath('/html/body/div[3]/div/div/div[2]/div/div/div/div/div[1]/div[1]/div[4]/div/span[2]')[0]
    driver.implicitly_wait(10)
    python_button.click()
    

    driver.quit()
    print("Driver Exited")

    return {}
