import os
from tex_parser import TexParser

def start_parsing(file):
    # os.system("pdflatex " + file)
    latex_parser = TexParser()
    print("TEST HERE")
    latex_parser.parse(file)
    # TODO
    # Get .aux file
    return file