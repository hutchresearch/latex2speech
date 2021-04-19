# # Run flask app: python3 application.py

# For uwsgi container to host flask in a production setting
# -> sudo apt-get install gcc (Need to have c compiler) -> If using mac command is sudo brew install gcc
# You also need the python development headers, to get this run the command or equivalent to apt-get install python-dev
# -> pip install uwsgi
import os, time
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
application = app
dropzone = Dropzone(app)

# Set iteration for file traversal
ITERATION = 3

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
    finalLog = glob.glob(app.config['CUSTOM_STATIC_PATH'] + "/*.log")

    for f in files:
        os.remove(f)

    for f in final:
        os.remove(f)

    for f in finalLog:
        os.remove(f)

# Helper function to compress files
def compress_holder(file, bib):
    together = []
    together.append(file)
    together.append(bib)
    return together

# Helper function to replace directory paths
def replace_path(compress, current_path, parent_path, path_files, iter):
    for f in path_files:
        extension = f.rsplit('.', 1)
        if len(extension) > 1 and f[:2] != '._':
            if extension[1] == 'tex':
                compress[0].append(f)
                os.replace(current_path + f, parent_path + f)
            elif extension[1] == 'bib':
                compress[1].append(f)
                os.replace(current_path + f, parent_path + f)
            elif extension[1] == 'zip':
                os.replace(current_path + f, parent_path + f)
                facilitate_zip_files(f, iter + 1, compress)
            elif extension[1] == 'tar':
                os.replace(current_path + f, parent_path + f)
                facilitate_tar_files(f, iter + 1, compress)

    shutil.rmtree(current_path)

    return compress

# 
def facilitate_zip_files(zip_folder, zip_iteration, compression):
    tempDirectory = 'zip_contents' + str(zip_iteration)

    with zipfile.ZipFile(os.getcwd() + '/upload/' + zip_folder, 'r') as zip_ref:
        os.makedirs(os.path.join(os.getcwd() + '/upload', tempDirectory))
        zip_ref.extractall(os.getcwd() + '/upload/' + str(tempDirectory))

    current_path = os.getcwd() + '/upload/' + str(tempDirectory) + '/'
    parent_path = os.getcwd() + '/upload/'

    path_files = os.listdir(current_path)
    files = replace_path(compress_holder(compression[0], compression[1]), current_path, parent_path, path_files, zip_iteration)

    return files

# 
def facilitate_tar_files(tar_folder, tar_iteration, compression):
    tempDirectory = 'tar_contents' + str(tar_iteration)

    with tarfile.open(os.getcwd() + '/upload/' + tar_folder) as tar:
        os.makedirs(os.path.join(os.getcwd() + '/upload', tempDirectory))
        tar.extractall(os.getcwd() + '/upload/' + tempDirectory)

    current_path = os.getcwd() + '/upload/' + tempDirectory + '/'
    parent_path = os.getcwd() + '/upload/'

    tar_directory = os.listdir(current_path)
    tar_contents_path = current_path + str(tar_directory[0] + '/')
    path_files = os.listdir(tar_contents_path)

    files = replace_path(compress_holder(compression[0], compression[1]), tar_contents_path, parent_path, path_files, tar_iteration)
    shutil.rmtree(current_path)

    return files

# 
def facilitate_upload(content, file_holder, bib_holder, iteration):
    if iteration == ITERATION:
        return compress_holder(file_holder, bib_holder)

    extension = content.rsplit('.', 1)

    if len(extension) > 1 and content[:2] != '._':
        if extension[1] == 'tex':
            file_holder.append(content)
        elif extension[1] == 'bib':
            bib_holder.append(content)
        elif extension[1] == 'zip':
            files = facilitate_zip_files(content, iteration, compress_holder(file_holder, bib_holder))
            file_holder = files[0]
            bib_holder = files[1]
        elif extension[1] == 'gz':
            split = content.split('.')
            
            if (split[len(split) - 2] != 'tar'):
                return 0

            files = facilitate_tar_files(content, iteration, compress_holder(file_holder, bib_holder))
            file_holder = files[0]
            bib_holder = files[1]

    return compress_holder(file_holder, bib_holder)

@app.route('/')
def index():
    print("HEY")
    return render_template('index.html')

# Upload middle man
@app.route('/upload', methods=['POST'])
def handle_upload():
    print("THIS RUNS?")
    session.pop('file_holder', None)
    session.pop('bib_holder', None)

    # Create upload directory (if non exists)
    if not os.path.exists('upload'):
        os.makedirs('upload')

    # Create session
    if 'file_holder' not in session:
        session['file_holder'] = []
    if 'bib_holder' not in session:
        session['bib_holder'] = []

    # Grabbing obj
    file_holder = session['file_holder']
    bib_holder = session['bib_holder']

    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
            files = facilitate_upload(f.filename, file_holder, bib_holder, 0)
            file_holder = files[0]
            bib_holder = files[1]

    return '', 204

# Download resulting output page
@app.route('/form', methods=['POST'])
def handle_form():
    # redirect to home if nothing in session
    if 'file_holder' not in session or session['file_holder'] == []:
        return redirect(url_for('index'))

    file_holder = session['file_holder']
    bib_holder = session['bib_holder']

    # Pop sessions 
    session.pop('file_holder', None)
    session.pop('bib_holder', None)

    # Render
    file_links = start_polly(file_holder, bib_holder)

    # redirect to home if nothing in file_links
    if file_links[0] == []:
        return redirect(url_for('index'))

    audio = file_links[1]
    master = file_links[0]

    file_audio = zip(master, audio)

    delete_from_folder()

    return render_template(
        'download.html',
        file_holder = file_audio)

if __name__ == '__main__':
    app.run(debug=True)