import os
import json
from flask import Blueprint
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



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
    driver.get("http://www.stocktwits.com")
    driver.implicitly_wait(10)

    # Login
    login_button = driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]

    driver.implicitly_wait(10)

    login_button.click()

    driver.implicitly_wait(10)

    user_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
    user_input.send_keys('145444')
    password_input = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
    password_input.send_keys('rtrtrtrrgrgrgr')
    password_input.send_keys(Keys.ENTER)
    # submit_button = driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]

    driver.implicitly_wait(10)

    submit_button.click()

    # driver.quit()
    print("Driver Exited")

    return {}
