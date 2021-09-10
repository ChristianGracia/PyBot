from flask import Flask, json
import os
from routes.post import post
from dotenv import load_dotenv

# Get the path to the directory this file is in
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))

test_var = os.getenv("TEST_VAR")

app = Flask(__name__)
app.register_blueprint(post, url_prefix='/post')

@app.route('/')
def main():
    return 'Stocktwits API Bot'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    
