import os, time, random, json, datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from time import sleep
from random import randint
import pydub
import urllib
from speech_recognition import Recognizer, AudioFile

from classes.stocktwits_response import StockTwitsResponse

class ChromeDriver:
    def __init__(self, username, password, data):
        self.driver = webdriver.Chrome(options=self.set_chrome_options(), executable_path=r"{}".format(os.getenv('CHROME_DRIVER_URL')))
        self.ticker = data['ticker']
        self.message = data['message']
        self.positive_sentiment = data['positive_sentiment']
        self.randomization = data['randomization']
        self.username = username
        self.password = password

        # Add random repeating character to post to avoid 60 min duplicate post limit
        if self.randomization:
            self.random_int = datetime.datetime.now().minute + datetime.datetime.now().second
            self.message += ''.join(random.choice("!") for i in range(self.random_int))

    def login_and_post_stocktwits(self):
        self.driver.set_window_size(1920, 1080)
        self.driver.get("https://www.stocktwits.com")
        self.login()
        # self.post()
        # self.driver.quit()

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

        time.sleep(1)
        password_input = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input')[0]
        password_input.send_keys(self.password)

        time.sleep(2)
        captcha_button = self.driver.find_elements_by_xpath("//iframe[starts-with(@name,'a-')]")[0]
        captcha_button.click()

        time.sleep(2)
        # audio_button = self.driver.find_elements_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[2]/button')[0]
        # audio_button.click()

        # self.driver.switch_to.default_content()

        # frames = self.driver.find_element_by_xpath(
        #     "/html/body/div[2]/div[4]").find_elements_by_tag_name("iframe")

        # sleep(randint(2, 4))

        # self.driver.switch_to.default_content()

        # frames = self.driver.find_elements_by_tag_name("iframe")

        # self.driver.switch_to.frame(frames[-1])

        # self.driver.find_element_by_id("recaptcha-audio-button").click()

        # self.driver.switch_to.default_content()

        # frames = self.driver.find_elements_by_tag_name("iframe")

        # self.driver.switch_to.frame(frames[-1])

        # sleep(randint(2, 4))

        # self.driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

        # try:
        #     src = self.driver.find_element_by_id("audio-source").get_attribute("src")
        #     print(src)
        #     urllib.request.urlretrieve(src, path+"\\audio.mp3")

        #     sound = pydub.AudioSegment.from_mp3(
        #         path+"\\audio.mp3").export(path+"\\audio.wav", format="wav")

        #     recognizer = Recognizer()

        #     recaptcha_audio = AudioFile(path+"\\audio.wav")

        #     with recaptcha_audio as source:
        #         audio = recognizer.record(source)

        #     text = recognizer.recognize_google(audio, language="de-DE")

        #     print(text)

        #     inputfield = self.driver.find_element_by_id("audio-response")
        #     inputfield.send_keys(text.lower())

        #     inputfield.send_keys(Keys.ENTER)

        #     sleep(10)
        #     print("Success")
        # except NameError:
        #     print("Failed")
        #     print(NameError)
        #     self.driver.quit()

        # submit_credentials_button = self.driver.find_elements_by_xpath('//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[2]/div[1]/button')[0]
        # submit_credentials_button.click()

        time.sleep(1)

    def create_response(self):
        response = StockTwitsResponse(self.ticker, 'Bullish' if self.positive_sentiment else 'Bearish', self.message, self.random_int if self.randomization else False)
        return json.dumps(response.__dict__)
        
    def set_chrome_options(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # ua = UserAgent()
        # userAgent = ua.random
        # print(userAgent)
        # chrome_options.add_argument(f'user-agent={userAgent}')
        # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36 Edge/12.10166"')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        return chrome_options
        
