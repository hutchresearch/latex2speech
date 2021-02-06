# General Libraries
from typing import Optional
import os
import sys
import requests
import json
import urllib.request

# AWS Libraries
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

# Parsing Library
from tex_parser import TexParser

# Creates session of user using AWS credentials
session = Session(aws_access_key_id='AKIAZMJSOFHCTDL6AQ4M', aws_secret_access_key='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', region_name='us-east-1')

# Creates objects of use
polly = session.client("polly")

# Path to upload
path = os.getcwd() + '/upload'

# Returns audio of file using Amazon Polly
# Feeding in marked up SSML document
def tts_of_file(file, contents):

    try:
        # Request speech synthesis
        audio = polly.synthesize_speech(
            VoiceId = "Joanna",
            OutputFormat = "mp3",
            TextType = "ssml",
            Text = contents)

        objectName = file + ".mp3"

        if "AudioStream" in audio:
            with closing(audio["AudioStream"]) as stream:
                output = objectName

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())  

                    # Download to user's local machine

                    # Delete file
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        return objectName

    except (BotoCoreError, ClientError) as error:
        # Error and exit
        print(error)
        sys.exit(-1)

# Gets contents of file, returns variable holding all text
# Converts bytes to string
def get_text_file(file):
    text = file.read()
    # return str(text, 'utf-8')
    return text

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(fileContents, bibContents):
    links = []
    latex_parser = TexParser()

    for file in fileContents:
        myFile = path + "/" + file
        fileObj = open(myFile, "r")

        # Call parser here
        parsed_contents = latex_parser.parse(fileObj.read(), bibContents)

        # Remove file
        os.remove(myFile)

        # print("\n\nCONTENTS AFTER CHANGE\n\n" + parsed_contents + "\n\n")

        # Feed to Amazon Polly here
        audio_link = tts_of_file(file, parsed_contents)
        # audio_link = "hi"
        links.append(audio_link)

    return links