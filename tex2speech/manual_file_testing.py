from expand_macros import normalize_doc_macros
from TexSoup import TexSoup

text = open('/home/mightymungus/latex2speech/tex2speech/Documentation/hundred_k_errors/aztec (copy).tex', 'r').read()
normalize_doc_macros(text)
# print(text[557:577])
# doc = TexSoup(text)