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

@post.route('/st', methods = ['POST']) 
def post_stocktwits():

    request_body = request.get_json()
    message = request_body['message']
    ticker = request_body['ticker']
    positive_sentiment = request_body['bullish']

    driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    driver.get("https://www.stocktwits.com")

    time.sleep(1)

    # Login
    login_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]
    login_button.click()

    # Enter login credentials
    user_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
    user_input.send_keys(os.getenv('ST_USERNAME'))
    password_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
    password_input.send_keys(os.getenv('ST_PASSWORD'))

    
    submit_credentials_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
    submit_credentials_button.click()

    time.sleep(1)

    formatted_message = "${} {}".format(ticker, message)

    sentiment_xpath = '//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[{}]'

    sentiment_button = driver.find_elements_by_xpath(sentiment_xpath.format(1 if positive_sentiment else 2))[0]
    sentiment_button.click()

    message_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[2]/div')[0]
    message_input.click()
    message_input.send_keys(formatted_message)
    
    submit_post_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[3]/div[1]/button')[0]
    submit_post_button.click()

    time.sleep(1)

    driver.quit()

    return 'Ticker: {}, Sentiment: {}, Post: {}'.format(ticker, 'bullish' if positive_sentiment else 'bearish', message)