import os, time, random, json, datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from classes.stocktwits_response import StockTwitsResponse

class ChromeDriver:
    def __init__(self, username, password, request_body):
        self.driver = webdriver.Chrome(options=self.set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))
        self.ticker = request_body['ticker']
        self.message = request_body['message']
        self.positive_sentiment = request_body['positive_sentiment']
        self.randomization = request_body['randomization']
        self.username = username
        self.password = password

        # Add random repeating character to post to avoid 60 min duplicate post limit
        if self.randomization:
            self.random_int = datetime.datetime.now().minute + datetime.datetime.now().second
            self.message += ''.join(random.choice("!") for i in range(self.random_int))

    def login_and_post_stocktwits(self):
        self.driver.get("https://www.stocktwits.com")
        self.login()
        self.post()
        self.driver.quit()

        return self.create_response()

    def post(self):
        formatted_message = "${} {}".format(self.ticker, self.message)

        sentiment_xpath = '//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[{}]'

        sentiment_button = self.driver.find_elements_by_xpath(sentiment_xpath.format(1 if self.positive_sentiment else 2))[0]
        sentiment_button.click()

        message_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[2]/div')[0]
        message_input.click()
        message_input.send_keys(formatted_message)
        
        submit_post_button = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[3]/div[1]/button')[0]
        submit_post_button.click()
        time.sleep(1)
    def spam(self):
        self.driver.get("https://www.stocktwits.com")
        self.login()

        print('30 seconds to get through captcha')
        time.sleep(30)

        print('loop starting')
        for x in range(30):
            self.post();
            time.sleep(15)
            print(self.create_response())

    def login(self):
        login_button = self.driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]
        login_button.click()

        user_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
        user_input.send_keys(self.username)
        password_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
        password_input.send_keys(self.password)

        # submit_credentials_button = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
        # submit_credentials_button.click()

        time.sleep(1)

    def create_response(self):
        response = StockTwitsResponse(self.ticker, 'Bullish' if self.positive_sentiment else 'Bearish', self.message, self.random_int if self.randomization else False)
        return json.dumps(response.__dict__)
        
    def set_chrome_options(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        return chrome_options
        
