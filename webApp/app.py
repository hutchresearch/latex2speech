# Run flask app: python3 -m flask run

from flask import Flask
from datetime import datetime
from flask import render_template
import re

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "main.html"
    )

# @app.route("/hello/")
# @app.route("/hello/<name>")
# def hello_there(name = None):
#     return render_template(
#         "main.html",
#         name=name,
#         date=datetime.now()
#     )