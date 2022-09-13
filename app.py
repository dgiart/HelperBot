from flask import Flask
from time import time
app = Flask(__name__)

@app.route('/')
def index():
    return f'new 13.09 at {time()}'

if __name__ == '__main__':
    app.run()