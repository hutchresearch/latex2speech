import os
import sys
sys.path.insert(1, "/Users/taichen/Desktop/Tai/Tex2Speech/latex2speech/app/latex-parser")
import tex_parser

def start_parsing(file):
    # os.system("pdflatex " + file)
    latex_Parser = tex_parser.TexParser()
    print("TEST HERE")
    # tex_parser.parse(file)
    # TODO
    # Get .aux file
    return file