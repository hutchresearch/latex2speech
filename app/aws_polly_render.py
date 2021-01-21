# General Libraries
from typing import Optional
import os
import sys
import requests

# AWS Libraries
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError

# Parsing Library
from parser_manager import start_parsing

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
    url = create_presigned_url(
        bucket_name,
        bucket_resource_url
    )

    return url


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
            TextType = "text",
            Text = "<speak>" + contents + "</speak>")

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

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(file):
    # Call parser here
    file = start_parsing(file)

    # Get contents of file
    contents = get_text_file(file)

    # print("\n\n" + contents)

    # Feed to Amazon Polly here
    # audio_link = tts_of_file(file, contents)
    audio_link = "hi"
    return audio_link