import os

# Changes .tex file to SSML file
def change_file_type(file):
    base = os.path.splitext(file)[0]
    os.rename(file, base + '.ssml')

    # Feed SSML file to amazon polly 

# Function that is called from app.py with file
# Adds beginner and end SSML tags
def start_polly(file):
    # Opens file adds tag to begin and end
    with open(file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        beginTag = "<speak>"
        f.write(beginTag.rstrip('\r\n') + '\n' + content + '\n</speak>')

    # Call parser here
    # newFile = start_parser(file)

    # Change .tex file to .SSML file here
    