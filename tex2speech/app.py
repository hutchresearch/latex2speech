# Run flask app: python3 -m flask run

from flask import Flask, render_template, request, make_response
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
@app.route("/download", methods = ['POST'])
def render_then_download():
    if request.method == 'POST':
        # Gets file, passes file to aws_polly_render
        file = request.files['file']
        audio_link = start_polly(file)

        # Displays download page, with audio
        return render_template(
            "download.html",
            audio_download = audio_link
        )

# If usr tries going to random page on our web application
# through page does not exist
@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                % page_name, 404)
    return response