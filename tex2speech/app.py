# # Run flask app: python3 -m flask run

import os
import glob
import zipfile
import shutil
import tarfile

from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_dropzone import Dropzone
from aws_polly_render import start_polly

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

app.config['CUSTOM_STATIC_PATH'] = os.path.join(basedir, '')
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'upload')

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'upload'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.tex, .bib, .zip, .gz',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

dropzone = Dropzone(app)

# Helper function to add values to each array
def add_to_array(uploadName, extension):
    array = []
    for file in request.files.getlist(uploadName):
        if file.filename != '':
            # Save file to upload folder
            file.save(os.path.join(app.config['UPLOADED_PATH'], file.filename))

            # Add to array
            if os.path.splitext(file.filename)[1] == extension:
                array.append(file.filename)

    return array

# Helepr function to delete files
def delete_from_folder():
    files = glob.glob(app.config['UPLOADED_PATH'] + "/*")
    final = glob.glob(app.config['CUSTOM_STATIC_PATH'] + "/*.tex")

    for f in files:
        os.remove(f)

    for f in final:
        os.remove(f)

def facilitate_zip_files(zip_folder, file_holder, bib_holder):
    with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
        os.makedirs(os.path.join(os.getcwd() + '/upload', 'zip_contents'))
        zip_ref.extractall(os.getcwd() + '/upload/zip_contents')

    current_path = os.getcwd() + '/upload/zip_contents/'
    parent_path = os.getcwd() + '/upload/'

    files = os.listdir(current_path)

    for f in files:
        extension = f.rsplit('.', 1)

        if len(extension) > 1:
            if extension[1] == 'tex':
                file_holder.append(f)
                os.replace(current_path + f, parent_path + f)
            elif extension[1] == 'bib':
                bib_holder.append(f)
                os.replace(current_path + f, parent_path + f)

    shutil.rmtree(current_path)

    together = []
    together.append(file_holder)
    together.append(bib_holder)

    return together

def facilitate_tar_files(tar_folder, file_holder, bib_holder):
    with tarfile.open(os.getcwd() + '/upload/' + tar_folder.filename) as tar:
        os.makedirs(os.path.join(os.getcwd() + '/upload', 'tar_contents'))
        tar.extractall(os.getcwd() + '/upload/tar_contents')

    current_path = os.getcwd() + '/upload/tar_contents/'
    parent_path = os.getcwd() + '/upload/'

    tar_directory = os.listdir(current_path)
    tar_contents_path = current_path + str(tar_directory[0] + '/')
    files = os.listdir(tar_contents_path)

    for f in files:
        print(f)
        extension = f.rsplit('.', 1)
        print(f[:2])
        if len(extension) > 1 and f[:2] != '._':
            if extension[1] == 'tex':
                file_holder.append(f)
                os.replace(tar_contents_path + f, parent_path + f)
            elif extension[1] == 'bib':
                bib_holder.append(f)
                os.replace(tar_contents_path + f, parent_path + f)

    shutil.rmtree(current_path)

    together = []
    together.append(file_holder)
    together.append(bib_holder)

    return together

@app.route('/')
def index():
    return render_template('index.html')

# Upload middle man
@app.route('/upload', methods=['POST'])
def handle_upload():
    session.pop('audio', None)
    session.pop('master', None)

    # Create upload directory (if non exists)
    if not os.path.exists('upload'):
        os.makedirs('upload')

    # Create session
    if 'audio' not in session:
        session['audio'] = []
    if 'master' not in session:
        session['master'] = []

    # Grabbing obj
    file_holder = []
    bib_holder = []
    audio_links = session['audio']
    master = session['master']

    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            extension = os.path.splitext(f.filename)[1]

            if extension == '.tex':
                file_holder.append(f.filename)
            elif extension == '.bib':
                bib_holder.append(f.filename)
            elif extension == '.zip':
                files = facilitate_zip_files(f, file_holder, bib_holder)
                file_holder = files[0]
                bib_holder = files[1]
            elif extension == '.gz':
                split = f.filename.split('.')
                
                if (split[len(split) - 2] != 'tar'):
                    return 0

                files = facilitate_tar_files(f, file_holder, bib_holder)
                file_holder = files[0]
                bib_holder = files[1]
    print(file_holder)
    print(bib_holder)
    # Render
    file_links = start_polly(file_holder, bib_holder)
    session['audio'] = file_links[1]
    session['master'] = file_links[0]

    return '', 204

# Download resulting output page
@app.route('/form', methods=['POST'])
def handle_form():
    # redirect to home if nothing in session
    if "audio" not in session or session['audio'] == []:
        return redirect(url_for('index'))

    audio = session['audio']
    master = session['master']

    # Pop sessions 
    session.pop('audio', None)
    session.pop('master', None)

    file_audio = zip(master, audio)

    delete_from_folder()

    return render_template(
        'download.html',
        file_holder = file_audio)

if __name__ == '__main__':
    app.run(debug=True)