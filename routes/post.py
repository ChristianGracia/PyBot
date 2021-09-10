import json, time, os
from flask import Blueprint, request

from classes.chrome_driver import ChromeDriver

post = Blueprint('post', __name__)

@post.route('/st', methods = ['POST']) 
def post_stocktwits():

    request_body = request.get_json()

    chrome_driver = ChromeDriver()

    return chrome_driver.post_stocktwits(
        os.getenv('ST_USERNAME'), os.getenv('ST_PASSWORD'), request_body['ticker'],
        request_body['message'], request_body['positive_sentiment'], request_body['randomization']
    )