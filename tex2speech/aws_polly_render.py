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
from pybtex.database.input import bibtex

import tex2speech.expand_labels
# Internal classes
from conversion_db import ConversionDB
from conversion_parser import ConversionParser

# Creates session of user using AWS credentials
session = Session(aws_access_key_id='AKIAZMJSOFHCTDL6AQ4M', aws_secret_access_key='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', region_name='us-east-1')

# Creates objects of use
polly = session.client("polly")
s3 = session.client("s3")

# Path to upload
path = os.getcwd() + '/upload'

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
            OutputS3KeyPrefix = file,
            OutputFormat = "mp3",
            TextType = "ssml",
            Text = contents)

        # Output the task ID
        taskId = audio['SynthesisTask']['TaskId']

        # Get audio link from bucket
        objectName = file + "." + taskId + ".mp3"
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
    # return str(text, 'utf-8')
    return text

# Parsing .bib files helper
def parse_bib_file(thePath):
    fileObj = open(thePath, "r")
    contents = fileObj.read()
    returnObj = ""
    
    parser = bibtex.Parser()
    bib_data = parser.parse_string(contents)
    returnObj += "<emphasis level='strong'> References Section </emphasis> <break time='1s'/> "
    
    # Looks at bib contents
    for entry in bib_data.entries.values():
        returnObj += " Bibliography item is read as: <break time='0.5s'/>" + entry.key + ". Type: " + entry.type + "<break time='0.5s'/> "

        # Gets authors
        for en in entry.persons.keys():
            returnObj += " Authors: "
            for author in bib_data.entries[entry.key].persons[en]:
                returnObj += str(author) + ", <break time='0.3s'/> "

        # Gets all other key - value pairs and reads them out
        for en in entry.fields.keys():
            returnObj += str(en) + ": " + str(bib_data.entries[entry.key].fields[en] + "<break time='0.3s'/>")

    os.remove(thePath)

    return returnObj

# Helper method used if found a corresponding input file
def found_input_file(line, outfile, i, input):
    tmp = ""  
    contained = False

    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if input/include keyword was found in list of fiels
        for inputFile in input:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".tex"):
                append = tmp + ".tex"

            if(append == inputFile):
                with open(path + "/" + inputFile,'r') as tmpInput:
                    outfile.write(tmpInput.read())
                    contained = True
                    tmpInput.close()
        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Input file not found \n")
        contained = True

    return contained

# Helper method used if found a corresponding bib file
# Will return inner file which records corresponding bib file,
# master file and if there was a bib or not
def found_bibliography_file(line, outfile, i, bib, innerFile):
    tmp = ""  
    contained = False
    
    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if bibliography keyword was found in list of fiels
        for bibFile in bib:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".bib"):
                append = tmp + ".bib"

            if(append == bibFile):
                thePath = path + "/" + bibFile
                # outfile.write(parse_bib_file(bibFile, thePath))
                innerFile.append(str(thePath))
                contained = True

        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Bibliography file not found \n")
        innerFile.append("")

    innerFile.append(str(contained))
    return innerFile

# Creates a list of master files to hold the uploaded main 
# files and input files that are referenced into a single 
# master file
#
# returns list of master files
def create_master_files(main, input, bib):
    masterFiles = []
    add = 0

    # For every uploaded main file
    for mainFile in main:
        add = add+1

        # Create new master file
        with open("final" + str(add) + ".tex", 'w') as outfile:
            innerFile = []
            innerFile.append("final" + str(add) + ".tex")
            with open(path + "/" + mainFile, 'r') as infile:
                # For each line, add to the master file
                for line in infile:
                    tmp = ""
                    contained = False  

                    for i in range(len(line)):
                        tmp = tmp + line[i]
                        i = i + 1
                        # Finds include or input file
                        if(tmp == "\\include{" or tmp == "\\input{"):
                            contained = found_input_file(line, outfile, i, input)

                        # Finds bibliography file
                        if(tmp == "\\bibliography{"):
                            innerFile = found_bibliography_file(line, outfile, i, bib, innerFile)
                            contained = innerFile[2]
                    
                    # Attach true or false of file if has corresponding bib
                    if(contained == "False"):          
                        outfile.write(line)
                        
            masterFiles.append(innerFile)

        outfile.close()
    return masterFiles

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(main, input, bibContents):
    links = []
    masterFiles = []

    masterFiles = create_master_files(main, input, bibContents)

    print(str(masterFiles))
    print(main[0])
    testing = open(path + "/" + main[0], "r")
    print(testing)

    # Create database/parser
    dbSource = open('static/pronunciation.xml')
    db = ConversionDB(dbSource.read())
    parser = ConversionParser(db)

    for master in masterFiles:
        # Expand Labels then open document
        # tex2speech.expand_labels.expandDocNewLabels(master)
        # texFile = open(master[0], "r")
        texFile = open("final1.tex", "r")

        print(texFile.read())
        # Call parsing here
        parsed_contents = parser.parse(texFile.read())

        if (len(master) > 1):
            parsed_contents += parse_bib_file(master[1])

        print("\n\nCONTENTS AFTER CHANGE\n\n" + parsed_contents + "\n\n")

        # Feed to Amazon Polly here
        # audio_link = tts_of_file(master, parsed_contents)
        audio_link = "hi" # I use hi because I don't want it to upload to S3 bucket right now :]
        links.append(audio_link)

    return links