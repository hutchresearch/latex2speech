# Run flask app: python3 -m flask run

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template(
        "main.html"
    )