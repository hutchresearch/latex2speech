import os
from tex_parser import TexParser

def start_parsing(file):
    # os.system("pdflatex " + file)
    latex_parser = TexParser()
    print("\nINITIAL RUNNING\n")

    parsed_text = latex_parser.parse(file)
    print("TEST HERE")
    # TODO
    # Get .aux file
    return parsed_text