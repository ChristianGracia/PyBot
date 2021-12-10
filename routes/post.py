import json, time, os
from flask import Blueprint, request

from classes.chrome_driver import ChromeDriver

post = Blueprint('post', __name__)

@post.route('/st', methods = ['POST']) 
def post_stocktwits():
    chrome_driver = ChromeDriver(os.getenv('ST_USERNAME'), os.getenv('ST_PASSWORD'), request.get_json())
    return chrome_driver.login_and_post_stocktwits()

@post.route('/spam', methods = ['POST']) 
def spam_ticker():
    chrome_driver = ChromeDriver(os.getenv('ST_USERNAME'), os.getenv('ST_PASSWORD'), request.get_json())
    chrome_driver.spam()