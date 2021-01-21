import os

def start_parsing(file):
    print("\n\nTEST")

    print(file.filename)
    os.system("pdflatex " + file)

    # TODO
    # Get .aux file
    return file