import json, time, os
from flask import Blueprint, request

from classes.chrome_driver import ChromeDriver

post = Blueprint('post', __name__)

@post.route('/st', methods = ['POST']) 
def post_stocktwits():

    request_body = request.get_json()

    message = request_body['message']
    ticker = request_body['ticker']
    positive_sentiment = request_body['positive_sentiment']
    randomization = request_body['randomization']

    chrome_driver = ChromeDriver()

    return chrome_driver.post_stocktwits(os.getenv('ST_USERNAME'), os.getenv('ST_PASSWORD'), ticker, message, positive_sentiment, randomization)