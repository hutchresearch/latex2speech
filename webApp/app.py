# Run flask app: python3 -m flask run

from flask import Flask, render_template, request

app = Flask(__name__)

# Render home page at start of use
@app.route("/")
def home():
    return render_template(
        "index.html"
    )

# Get file after download, feed it to parser
# Display download.html file
@app.route("/submit", methods = ['POST'])
def render_then_download():
    if request.method == 'POST':
        f = request.files['file']

    return render_template(
        "download.html"
    )