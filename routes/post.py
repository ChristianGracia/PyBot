from flask import Blueprint
import json

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import os


post = Blueprint('post', __name__)

def set_chrome_options() -> None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


@post.route('/st') 
def post_stocktwits():
    driver = webdriver.Chrome(options=set_chrome_options())
    driver.get("https://google.co.in")

    return "posting"

class JSONObject:  
  def __init__( self, dict ):  
      vars(self).update( dict )