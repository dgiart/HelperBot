from flask import Flask
from time import time, asctime
app = Flask(__name__)

@app.route('/')
def index():
    return f'<h1> New 13.09 at {asctime()} </h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0')