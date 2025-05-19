from flask import Flask

import pages

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world"