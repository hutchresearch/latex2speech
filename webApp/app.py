# Run flask app: python3 -m flask run

from flask import Flask, render_template, request, redirect, url_for, make_response, flash

app = Flask(__name__)

# Render home page at start of use
@app.route("/")
def home():
    return render_template(
        "index.html"
    )

# Get file after download, feed it to parser
# Display download.html file
@app.route("/submit")
def render_then_download():
    return render_template(
        "download.html"
    )