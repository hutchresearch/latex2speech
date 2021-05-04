# General Libraries
from typing import Optional
import os
import sys
import requests
import json, time
import urllib.request
import argparse
import re

# AWS Libraries
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

# Parsing Library
from pybtex.database.input import bibtex

from expand_labels import expand_doc_new_labels
from doc_cleanup import cleanxml_string
from format_master_files import format_master_files
# Internal classes
from conversion_db import ConversionDB
from conversion_parser import ConversionParser

# Creates session of user using AWS credentials
session = Session(profile_name='default')

# Creates objects of use
polly = session.client("polly")
s3 = session.client("s3")

# Check to see if file has been uplaoded to the S3 bucket or not
def check_s3(key):
    try:
        s3.head_object(Bucket="tex2speech", Key=key)
    except ClientError as e:
        return False
    return True

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
def tts_of_file(file, contents, last_file):
    try:
        # Request speech synthesis
        audio = polly.start_speech_synthesis_task(
            VoiceId = 'Joanna',
            OutputS3BucketName = 'tex2speech',
            OutputS3KeyPrefix = file,
            OutputFormat = 'mp3',
            TextType = 'ssml',
            Text = '<speak>' + contents + '</speak>')

        # Output the task ID
        task_id = audio['SynthesisTask']['TaskId']

        # Get audio link from bucket
        object_name = file + '.' + task_id + '.mp3'
        audio_link = generate_presigned_url(object_name)

        if last_file:
            while(not check_s3(object_name)):
                time.sleep(1)

        return audio_link

    except (BotoCoreError, ClientError, Exception) as error:
        # Error and exit
        print(error)
        sys.exit(-1)

# Gets contents of file, returns variable holding all text
# Converts bytes to string
def get_text_file(file):
    text = file.read()
    # return str(text, 'utf-8')
    return text

# Parsing .bib files helper
def parse_bib_file(the_path):
    file_obj = open(the_path, "r")
    contents = file_obj.read()
    return_obj = ""
    
    parser = bibtex.Parser()
    bib_data = parser.parse_string(contents)
    return_obj += "<emphasis level='strong'> References Section </emphasis> <break time='1s'/> "
    
    # Looks at bib contents
    for entry in bib_data.entries.values():
        return_obj += " Bibliography item is read as: <break time='0.5s'/>" + entry.key + ". Type: " + entry.type + "<break time='0.5s'/> "

        # Gets authors
        for en in entry.persons.keys():
            return_obj += " Authors: "
            for author in bib_data.entries[entry.key].persons[en]:
                return_obj += str(author) + ", <break time='0.3s'/> "

        # Gets all other key - value pairs and reads them out
        for en in entry.fields.keys():
            return_obj += str(en) + ": " + str(bib_data.entries[entry.key].fields[en] + "<break time='0.3s'/>")

    return return_obj

# Pass off to parser
def start_conversion(contents):
    # Create database/parser
    db_source = open('static/pronunciation.xml')
    db = ConversionDB(db_source.read())
    parser = ConversionParser(db)

    parsed_contents = parser.parse(contents)
    return parsed_contents

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(main, bib_contents):
    retObj = []
    links = []
    counter = 0
    end = False

    master_files = format_master_files(main, bib_contents)

    for master in master_files[1]:
        counter += 1

        if counter == len(master_files[0]):
            end = True 
        
        # Expand Labels then open document
        expand_doc_new_labels(master[0])
        tex_file = open(master[0], "r")

        # Call parsing here
        parsed_contents = start_conversion(tex_file.read())
        if (len(master) > 1 and master[2] == 'True'):
            parsed_contents += parse_bib_file(master[1])

        parsed_contents = cleanxml_string(parsed_contents)

        print("\n\nCONTENTS AFTER CHANGE\n\n" + parsed_contents + "\n\n")

        # Feed to Amazon Polly here
        # audio_link = tts_of_file(master[0], parsed_contents, end)
        audio_link = "hi"
        links.append(audio_link)

    retObj.append(master_files[0])
    retObj.append(links)

    return retObj
