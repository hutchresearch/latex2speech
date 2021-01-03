import os

# Returns audio of file using Amazon Polly
# Feeding in marked up SSML document
def tts_of_file(file):
    audio = "hi.mp4"
    return audio

# Changes .tex file to SSML file
def change_file_type(file):
    base = os.path.splitext(file)[0]
    os.rename(file, base + '.ssml')

    return file

# Adds begin and end tag to file
def add_begin_end_tags(file):
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        beginTag = "<speak>"
        f.write(beginTag.rstrip('\r\n') + '\n' + content + '\n</speak>')

    return file

# Function that is called from app.py with file
# Manages all tasks afterwords
def start_polly(file):
    file = add_begin_end_tags(file)

    # Call parser here
    # file = start_parser(file)

    # Change .tex file to .SSML file here
    file = change_file_type(file)

    # Feed to Amazon Polly here
    audio = tts_of_file(file)

    return audio 
    