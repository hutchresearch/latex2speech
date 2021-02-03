# Run flask app: python3 -m flask run

from flask import Flask, render_template, request, make_response, session, url_for
from aws_polly_render import start_polly
from flask_dropzone import Dropzone

app = Flask(__name__)
dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.tex'

app.config['SECRET_KEY'] = 'something_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    # List to hold our files
    file_holder = []

    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            tempFile = []
            file = request.files.get(f)
            tempFile.append(file)

            # If radio == yes (has .bib)
            # Append .bib file
                # tempFile.append(bib)

            file_holder.append(tempFile)
            print (file.filename)
        return "uploading..."
    return render_template('index.html')
    
@app.route('/download')
def results():
    print("Is this running??\n")
    return 0
    # return render_template('download.html')

# # Render home page at start of use
# @app.route("/")
# def home():
#     return render_template(
#         "index.html"
#     )

# # Get file after download, feed it to parser
# # Display download.html file
# @app.route("/download", methods = ['POST'])
# def render_then_download():
#     if request.method == 'POST':
#         # Gets file, passes file to aws_polly_render
#         file = request.files['file']
#         audio_link = start_polly(file)

#         # Displays download page, with audio
#         return render_template(
#             "download.html",
#             audio_download = audio_link
#         )

# # If usr tries going to random page on our web application
# # through page does not exist
# @app.route('/<page_name>')
# def other_page(page_name):
#     response = make_response('The page named %s does not exist.' \
#                 % page_name, 404)
#     return response