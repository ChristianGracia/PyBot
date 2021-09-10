import os, time, random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def set_chrome_options() -> None:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    return chrome_options

class ChromeDriver:
    def __init__(self):
        self.driver = webdriver.Chrome(options=set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))  
    def post_stocktwits(self, username, password, ticker, message, positive_sentiment, randomization):
        self.driver.get("https://www.stocktwits.com")

        time.sleep(1)

        # Login
        login_button = self.driver.find_elements_by_xpath('//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button')[0]
        login_button.click()

        # Enter login credentials
        user_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input')[0]
        user_input.send_keys(username)
        password_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
        password_input.send_keys(os.getenv('ST_PASSWORD'))

        
        submit_credentials_button = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
        submit_credentials_button.click()

        time.sleep(1)

        # Add random repeating character to post to avoid 60 min duplicate post limit
        if randomization:
            message += ''.join(random.choice("!") for i in range(random.randint(0, 50)))

        formatted_message = "${} {}".format(ticker, message)

        sentiment_xpath = '//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[1]/div/div[{}]'

        sentiment_button = self.driver.find_elements_by_xpath(sentiment_xpath.format(1 if positive_sentiment else 2))[0]
        sentiment_button.click()

        message_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div/div/div[2]/div')[0]
        message_input.click()
        message_input.send_keys(formatted_message)
        
        submit_post_button = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[3]/div/div/div[1]/div/div/div[1]/div/div[3]/div[1]/button')[0]
        submit_post_button.click()

        time.sleep(1)

        self.driver.quit()

        return 'Ticker: {}, Sentiment: {}, Post: {}'.format(ticker, 'bullish' if positive_sentiment else 'bearish', message)
        
