# Run flask app: python3 -m flask run

from flask import Flask, render_template, request, make_response, session, url_for, redirect
from aws_polly_render import start_polly
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.tex, .bib'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'

app.config['SECRET_KEY'] = 'something_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    # # set session for results
    if "file_holder" not in session:
        session['file_holder'] = {}

    if "bilb_holder" not in session:
        session['bib_holder'] = {}

    # # List to hold our files
    file_holder = session['file_holder']
    bib_holder = session['bib_holder']

    file_holder = {}

    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            if os.path.splitext(file.filename)[1] == ".tex":
                hashObject = []
                hashObject.append(str(file.read(), 'utf-8'))
                file_holder[file.filename] = hashObject
                # print("Tex file")

            elif os.path.splitext(file.filename)[1] == ".bib":
                # Hashtable of bib files
                hashObject = []
                hashObject.append(file.read())
                bib_holder[os.path.splitext(file.filename)[0]] = hashObject
                # print("Bib file")

        # Add files to session
        session['file_holder'] = file_holder
        session['bib_holder'] = bib_holder
        return "uploading..."

    return render_template(
        'index.html'
    )
    
@app.route('/download')
def results():
    # redirect to home if no images to display
    if "file_holder" not in session or session['file_holder'] == []:
        return redirect(url_for('index'))
        
    # set the file_urls and remove the session variable
    file_holder = session['file_holder']
    bib_holder = session['bib_holder']

    audio_links = start_polly(file_holder, bib_holder, len(bib_holder))

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