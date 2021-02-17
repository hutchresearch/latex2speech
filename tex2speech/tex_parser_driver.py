import sys

#from parser import Parser
from tex_parser import TexParser

parser = TexParser()
output = None
with open(sys.argv[1], "r") as texFile:
    output = parser.parse(texFile)

with open(sys.argv[2], "w") as outFile:
    outFile.write(output)

print("Wrote SSML to " + sys.argv[2])