import os
import json
import time
from flask import Blueprint
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
    return chrome_options

@post.route('/st') 
def post_stocktwits():
    driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    driver.get("https://www.stocktwits.com")
    driver.implicitly_wait(5)

    # Login
    login_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]

    login_button.click()

    user_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
    user_input.send_keys(os.getenv('ST_USERNAME'))
    password_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
    password_input.send_keys(os.getenv('ST_PASSWORD'))
    # password_input.send_keys(Keys.ENTER)
    submit_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
    submit_button.click()

    time.sleep(5)

    # Navigate to wanted Stock Symbol
    ticker = 'SPY'
    post_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div/div[5]/div[1]/span/button')[0]

    post_button.click()
    # driver.get("https://stocktwits.com/symbol/{}".format(ticker))
    # time.sleep(5)

    # Post Message
    message = "${} Bullish".format(ticker)
    # driver.findElement(By.xpath("//*[@id='app']/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]")).click();
    # post_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div/div[5]/div[1]/span/button')[0]
    # post_button.click()
    # message_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/input')[0]
    # message_input.send_keys(message)
    
    # submit_post_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/div[2]/div/div[3]/div[1]/button')[0]
    # submit_post_button.click()

    driver.quit()

    return 'Post: {}'.format(message)
