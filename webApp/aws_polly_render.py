from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

session = Session(profile_name="admin_user")
polly = session.client("polly")

# Returns audio of file using Amazon Polly
# Feeding in marked up SSML document
def tts_of_file(file):
    try:
        # Request speech synthesis
        audio = polly.synthesize_speech(Text="Hello world!", OutputFormat="mp3", VoiceId="Joanna")

        return audio
        
    except (BotoCoreError, ClientError) as error:
        # Error and exit
        print(error)
        sys.exit(-1)

# Changes .tex file to SSML file
def change_file_type(file):
    base = os.path.splitext(file.filename)[0]
    os.rename(file.filename, base + '.ssml')

    return file

# Adds begin and end tag to file
def add_begin_end_tags(file):
    with open(file.filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        beginTag = "<speak>"
        f.write(beginTag.rstrip('\r\n') + '\n' + content + '\n</speak>')

    return file

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(file):
    # Adds SSML tags to beginning/end
    # file = add_begin_end_tags(file)

    # Call parser here
    # file = start_parser(file)

    # Change .tex file to .SSML file here
    # file = change_file_type(file)

    # Feed to Amazon Polly here
    audio = tts_of_file(file)

    return audio 
    