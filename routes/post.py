import os
import json
import time
from flask import Blueprint, request
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

post = Blueprint('post', __name__)

def set_chrome_options() -> None:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    return chrome_options

@post.route('/st') 
def post_stocktwits():

    request_body = request.get_json()
    print(request_body)

    driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    driver.get("https://www.stocktwits.com")
    driver.implicitly_wait(5)

    # Login
    login_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]
    login_button.click()

    # Enter login credentials
    user_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
    user_input.send_keys(os.getenv('ST_USERNAME'))
    password_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
    password_input.send_keys(os.getenv('ST_PASSWORD'))

    
    submit_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
    submit_button.click()

    time.sleep(3)

    message = "${} {}".format(request_body['ticker'], request_body['message'])

    sentiment_xpath = '//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[{}]'

    sentiment_button = driver.find_elements_by_xpath(sentiment_xpath.format(1 if request_body['bullish'] else 2))[0]
    sentiment_button.click()

    message_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[2]/div')[0]
    message_input.click()
    message_input.send_keys(message)
    
    submit_post_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[3]/div[1]/button')[0]
    # submit_post_button.click()

    time.sleep(3)

    driver.quit()

    return 'Post: {}'.format(message)
