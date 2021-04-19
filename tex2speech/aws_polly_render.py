# General Libraries
from typing import Optional
import os
import sys
import requests
import json
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
# Internal classes
from conversion_db import ConversionDB
from conversion_parser import ConversionParser

# Creates session of user using AWS credentials
session = Session(profile_name='default')

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

# Helper method used if found a corresponding input file
def found_input_file(line, outfile, i, input):
    tmp = ""  
    contained = False

    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if input/include keyword was found in list of fiels
        for input_file in input:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".tex"):
                append = tmp + ".tex"

            if(append == input_file):
                with open(path + "/" + input_file,'r') as tmp_input:
                    contents = tmp_input.read().replace('%', 'Begin Comment ')
                    contents = contents.replace('\\LaTeX\\', '\\LaTeX')
                    outfile.write(contents)
                    contained = True
                    tmp_input.close()
        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Input file not found \n")

# Helper method used if found a corresponding bib file
# Will return inner file which records corresponding bib file,
# master file and if there was a bib or not
def found_bibliography_file(line, outfile, i, bib, inner_file):
    tmp = ""  
    contained = False
    
    while(line[i] != '}'):
        tmp = tmp + line[i]                          

        # Checks if bibliography keyword was found in list of fiels
        for bib_file in bib:
            append = tmp

            if(tmp[len(tmp)-3:len(tmp)] != ".bib"):
                append = tmp + ".bib"

            if(append == bib_file):
                the_path = path + "/" + bib_file
                inner_file.append(str(the_path))
                contained = True

        i = i + 1

    if(contained == False):
        outfile.write(tmp + " Bibliography file not found \n")
        inner_file.append("")

    inner_file.append(str(contained))
    return inner_file

# Function to check if the command is equal
def check(tmp, cmd):
    if tmp == cmd[:len(tmp)]:
        return True 
    return False

# Get rid of extra \ at end of words
def rid_of_back_backslash(line, i, potential):
    # Get end of line slashes out
    if i > 0 and line[i - 1] == ' ' and line[i] == '\\':
        potential = 'True'

    if line[i] == ' ':
        potential = 'False'

    if i < len(line) and potential == 'True' and line[i] == '\\' and line[i + 1] == ' ':
        potential = 'Changed'

    return potential

# Checks each document to see if the file is a main document or input document
# This is denoted by \begin{document} and \end{document} as main, and not if input
# Returns the array of all master files and input files
def find_master_files(main):
    total = []
    master = []
    input_list = []
    for filename in main:
        with open(path + '/' + filename, 'r') as file:
            contents = file.read()
            if r'\begin{document}' in contents and r'\end{document}' in contents:
                master.append(filename)
            else:
                input_list.append(filename)
            file.close()

    total.append(master)
    total.append(input_list)
    
    return total

# Creates a list of master files to hold the uploaded main 
# files and input files that are referenced into a single 
# master file
#
# returns list of master files
def create_master_files(main_input, bib):
    main = main_input[0]
    input_file = main_input[1]
    master_files = []

    add = 0
    potential = 'False'

    # For every uploaded main file
    for main_file in main:
        add = add + 1

        # Create new master file
        with open("final" + str(add) + ".tex", 'w') as outfile:
            inner_file = []
            inner_file.append("final" + str(add) + ".tex")
            with open(path + "/" + main_file, 'r') as in_file:
                # For each line, add to the master file
                for line in in_file:
                    tmp = ""

                    for i in range(len(line)):
                        potential = rid_of_back_backslash(line, i, potential)
                        if (potential == 'Changed'):
                            i = i + 1
                            potential = 'False'

                        tmp = tmp + line[i]

                        # Handle comments
                        if tmp == "%":
                            if len(line) > 2:
                                outfile.write("Start of comment " + line[1:].replace("%", ""))
                            break

                        if not check(tmp, r"\include{") and not check(tmp, r"\input{") and not check(tmp, r"\bibliography{"):
                            outfile.write(tmp)
                            tmp = ""

                        i = i + 1
                        # Finds include or input file
                        if (tmp == "\\include{" or tmp == "\\input{"):
                            found_input_file(line, outfile, i, input_file)

                        # Finds bibliography file
                        if (tmp == "\\bibliography{"):
                            inner_file = found_bibliography_file(line, outfile, i, bib, inner_file)
                        
            master_files.append(inner_file)

        outfile.close()
    return master_files

# Pass off to parser
def start_conversion(contents):
    # Create database/parser
    db_source = open('static/pronunciation.xml')
    db = ConversionDB(db_source.read())
    parser = ConversionParser(db)

    parsed_contents = parser.parse(contents)
    return parsed_contents

def def_main(master_name):
    with open(master_name, mode ='r+') as master:
        data = master.read()
        data = def_convert(data)

        master.seek(0)
        master.write(data)
        master.truncate()

def def_convert(text):
    return re.sub(
        r'\\def[\s]*(?P<name>\\[a-zA-Z]+)[\s]*(?P<args>(\[?#[0-9]\]?)*)[\s]*(?P<repl>\{.*\})',
        def_replace,
        text
    )

def def_replace(match):
    out = r'\newcommand{' + match.group('name') + r'}'
    if match.group('args'):
        max_arg = 1
        for c in match.group('args'):
            try:
                arg = int(c)
                if arg > max_arg:
                    max_arg = arg
            except ValueError:
                pass
        out += r'[{}]'.format(max_arg)
    out += match.group('repl')
    print(out)
    return out
    

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(main, bib_contents):
    retObj = []
    links = []

    main_input_files = find_master_files(main)
    master_files = create_master_files(main_input_files, bib_contents)

    print(master_files)

    for master in master_files:
        def_main(master[0])
        expand_doc_new_labels(master[0])
        tex_file = open(master[0], "r")

        # Call parsing here
        parsed_contents = start_conversion(tex_file.read())
        if (len(master) > 1 and master[2] == 'True'):
            parsed_contents += parse_bib_file(master[1])

        parsed_contents = cleanxml_string(parsed_contents)

        print("\n\nCONTENTS AFTER CHANGE\n\n" + parsed_contents + "\n\n")

        # Feed to Amazon Polly here
        # audio_link = tts_of_file(master[0], parsed_contents)
        audio_link = "hi"
        links.append(audio_link)

    retObj.append(main_input_files[0])
    retObj.append(links)

    return retObj
