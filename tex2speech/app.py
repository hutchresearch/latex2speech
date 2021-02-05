# Run flask app: python3 -m flask run

from flask import Flask, render_template, request, make_response, session, url_for, redirect
from aws_polly_render import start_polly
from flask_dropzone import Dropzone
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.tex, .bib'
# app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
# Uploads settings
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/upload'

app.config['SECRET_KEY'] = 'something_here'

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/download', methods=['POST'])
def results():
    file_obj = request.files
    file_holder = []
    bib_holder = []

    for f in file_obj:
        file = request.files.get(f)
        print(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        if os.path.splitext(file.filename)[1] == ".tex":
            file_holder.append(file.filename)
        elif os.path.splitext(file.filename)[1] == ".bib":
            bib_holder.append(file.filename)

    audio_links = start_polly(file_holder, bib_holder)

    return render_template(
        'download.html',
        file_audio = zip(file_holder, audio_links))

# If usr tries going to random page on our web application
# through page does not exist
@app.route('/<page_name>')
def other_page(page_name):
    response = make_response('The page named %s does not exist.' \
                % page_name, 404)
    return response