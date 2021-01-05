# General Libraries
from typing import Optional
import os
import sys
import requests

# AWS Libraries
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError

# Creates session of user using AWS credentials
session = Session(aws_access_key_id='AKIAZMJSOFHCTDL6AQ4M', aws_secret_access_key='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', region_name='us-east-1')

# Creates objects of use
polly = session.client("polly")
s3 = session.client("s3")

# Generate a presigned URL for the S3 object so any user can download
def create_presigned_url(bucket_name, object_name, expiration=3600):    
    try:
        # Creates s3 client, passes in arguments
        response = s3.generate_presigned_url('get_object', Params={
                                                    'Bucket': bucket_name,
                                                    'Key': object_name},
                                                    ExpiresIn = expiration)
    except ClientError as e:
        # Error and exit
        print(e)
        return None

    print("\n\n" + response + "\n\n")

    # The response contains the presigned URL
    return response

# Function that will get bucket information
# Then call helper to generate url
def generate_presigned_url(objectURL):
    bucket_name = "tex2speech"
    bucket_resource_url = objectURL
    # url = create_presigned_url(
    #     bucket_name,
    #     bucket_resource_url
    # )

    url = create_presigned_url(bucket_name, bucket_resource_url)
    if url is not None:
        response = requests.get(url)

    return response

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

        # ----- PRINT HELPERS FOR TESTING PURPOSES -----
        # Output the task ID
        taskId = audio['SynthesisTask']['TaskId']
        # print(f'Task id is {taskId}')

        # Retrieve and output the current status of the task
        # task_status = polly.get_speech_synthesis_task(TaskId = taskId)
        # print(f'Status: {task_status}')

        # Get audio link from bucket
        objectName = file.filename + "." + taskId + ".mp3"
        audio_link = generate_presigned_url(objectName)

        return audio_link

    except (BotoCoreError, ClientError) as error:
        # Error and exit
        print(error)
        sys.exit(-1)

# Gets contents of file, returns variable holding all text
# Converts bytes to string
def get_text_file(file):
    text = file.read()
    return str(text, 'utf-8')

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
    audio_link = tts_of_file(file, contents)

    return audio_link