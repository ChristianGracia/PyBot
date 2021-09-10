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

class StockTwitsResponse:
    def __init__(self, ticker, sentiment, message, randomization):
        self.ticker = ticker
        self.sentiment = sentiment
        self.message = message
        self.randomization = randomization

