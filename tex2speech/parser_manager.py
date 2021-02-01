import os
from tex_parser import TexParser

def start_parsing(file):
    # os.system("pdflatex " + file)
    latex_parser = TexParser()

    parsed_text = latex_parser.parse(file.read())

    # TODO
    # Get .aux file
    return parsed_text