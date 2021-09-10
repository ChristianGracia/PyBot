from flask import Blueprint
import json

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import os


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
    # driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    # driver.get("http://www.stocktwits.com") 
    # driver.quit()
    print("Driver Exited")

    return {}
