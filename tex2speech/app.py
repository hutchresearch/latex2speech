# # Run flask app: python3 -m flask run

import os
import glob

from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_dropzone import Dropzone
from aws_polly_render import start_polly

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.tex, .bib',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

dropzone = Dropzone(app)
app.config['SECRET_KEY'] = 'mah_key'
app.config['CUSTOM_STATIC_PATH'] = os.path.join(basedir, 'upload')

@app.route('/')
def index():
    return render_template('index.html')

# Upload middle man
@app.route('/upload', methods=['POST'])
def handle_upload():
    print("THIS RAN??")
    session.pop('file_holder', None)
    session.pop('audio', None)
    # Create session
    if "file_holder" not in session:
        session['file_holder'] = []
    if "audio" not in session:
        session['audio'] = []

    # Grabbing obj
    file_holder = session['file_holder']
    input_holder = []
    bib_holder = []
    audio_links = session['audio']
    print("yo???")

    req = request.form 
    print(req)
    for file in request.files.getlist('file'):
        print(file.filename)

    # for key, f in request.files.items():
    #     if key.startswith('file'):
    #         f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))

    #         if os.path.splitext(f.filename)[1] == ".tex":
    #             file_holder.append(f.filename)
    #         elif os.path.splitext(f.filename)[1] == ".bib":
    #             bib_holder.append(f.filename)

    # Render
    # audio_links = start_polly(file_holder, bib_holder)
    # session['file_holder'] = file_holder
    # session['audio'] = audio_links
    return render_template('download.html')
    # return '', 204

# Download resulting output page
@app.route('/form', methods=['POST'])
def handle_form():
    # redirect to home if nothing in session
    if "file_holder" not in session or session['file_holder'] == []:
        return redirect(url_for('index'))

    file_holder = session['file_holder']
    audio = session['audio']

    # Pop sessions 
    session.pop('file_holder', None)
    session.pop('audio', None)

    file_audio = zip(file_holder, audio)

    files = glob.glob(app.config['UPLOADED_PATH'] + "/*")
    for f in files:
        os.remove(f)

    return render_template(
        'download.html',
        file_holder = file_audio)

if __name__ == '__main__':
    app.run(debug=True)