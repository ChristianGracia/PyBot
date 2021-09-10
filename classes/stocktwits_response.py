import os, time, random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class StockTwitsResponse:
    def __init__(self, ticker, sentiment, message, randomization):
        self.ticker = ticker
        self.sentiment = sentiment
        self.message = message
        self.randomization = randomization

