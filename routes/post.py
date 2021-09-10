import json, time, os
from flask import Blueprint, request

from classes.chrome_driver import ChromeDriver

post = Blueprint('post', __name__)

@post.route('/st', methods = ['POST']) 
def post_stocktwits():
    chrome_driver = ChromeDriver()
    return chrome_driver.post_stocktwits(os.getenv('ST_USERNAME'), os.getenv('ST_PASSWORD'), request.get_json())