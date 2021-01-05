import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Creates session of user using AWS credentials
session = Session(aws_access_key_id='AKIAZMJSOFHCTDL6AQ4M', aws_secret_access_key='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', region_name='us-east-1')

# Creates objects of use
polly = session.client("polly")
s3 = session.client("s3")

# Returns audio of file using Amazon Polly
# Feeding in marked up SSML document
def tts_of_file(file, contents):

    try:
        # Request speech synthesis
        audio = polly.start_speech_synthesis_task(
            VoiceId = "Joanna",
            OutputS3BucketName = "tex2speech",
            OutputS3KeyPrefix = file.filename,
            OutputFormat = "mp3",
            Text = contents)

        # Output the task ID
        taskId = audio['SynthesisTask']['TaskId']
        print(f'Task id is {taskId}')

        # Retrieve and output the current status of the task
        task_status = polly.get_speech_synthesis_task(TaskId = taskId)
        print(f'Status: {task_status}')

        return audio

    except (BotoCoreError, ClientError) as error:
        # Error and exit
        print(error)
        sys.exit(-1)

# Gets contents of file, returns variable holding all text
def get_text_file(file):
    return file.read()

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

    # Get contents of file
    contents = get_text_file(file)

    # Feed to Amazon Polly here
    audio = tts_of_file(file, contents)

    return audio; 
    