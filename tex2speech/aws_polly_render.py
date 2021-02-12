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

        # ----- PRINT HELPERS FOR TESTING PURPOSES -----
        # Output the task ID
        taskId = audio['SynthesisTask']['TaskId']
        # print(f'Task id is {taskId}')

        # Retrieve and output the current status of the task
        # task_status = polly.get_speech_synthesis_task(TaskId = taskId)
        # print(f'Status: {task_status}')

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

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(main, input, bibContents):
    links = []
    latex_parser = TexParser()
    masterFiles = []
    
    #since every main file -> master file
    #make a list of the resulting master files
    #iterate through to send to parser

    #masterFiles = multiFile(main,input)

    add = 0
    add = add+1
        with open("final"+str(add)+".tex", 'w') as outfile:
            masterFiles.append(outfile)
            with open(path + "\\"+mainFile, 'r') as infile:

                for line in infile:
                    tmp = ""
                    contained = False  
                    for i in range(len(line)):
                    
                        tmp = tmp + line[i]
                        i = i + 1
                    
                        if(tmp == "\\include{" or tmp == "\\input{"):
                            tmp = ""                                             
                        

                            while(line[i] != '}'):
                                tmp = tmp + line[i]
                                print(tmp)                            

                                for inputFile in input:
                                    append = tmp
                                    if(tmp[len(tmp)-3:len(tmp)] != ".tex"):
                                        append = tmp + ".tex"
                                    if(append == inputFile):
                                        with open(inputFile,'r') as tmpInput:
                                            outfile.write(tmpInput.read())
                                            contained = True
                                            tmpInput.close()

                                i = i + 1

                            if(contained == False):
                                outfile.write(tmp + "File not found \n")
                                contained = True
                    
                                
                        

                    if(contained == False):          
                        outfile.write(line)
                    
        outfile.close()
    for master in masterFiles: 
        fileObj = open(master, "r")

        # Call parser here
        parsed_contents = latex_parser.parse(fileObj.read(), bibContents)

        # print("\n\nCONTENTS AFTER CHANGE\n\n" + parsed_contents + "\n\n")

        # Feed to Amazon Polly here
        # audio_link = tts_of_file(file, parsed_contents)
        audio_link = "hi"
        # links.append(audio_link)

        # Remove file
        # os.remove(myFile)

    return links

if __name__ == '__main__':
    main = []
    input = []
    bib = []
    start_polly(main, input, bib)