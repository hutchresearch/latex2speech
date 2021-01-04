# Run flask app: python3 -m flask run

from flask import Flask, render_template, request
from aws_polly_render import start_polly

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
        # Gets file, passes file to aws_polly_render
        file = request.files['file']
        audio = start_polly(file)
        print("123123123123")
        print(audio)
        # Displays download page, with audio
        return render_template(
            "download.html",
            audio_download = audio
        )