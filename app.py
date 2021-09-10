from flask import Flask
from routes.post import post
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(post, url_prefix='/post')

@app.route('/')
def main():
    return 'Stocktwits API Bot'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)