# TeX2Speech
A web app for converting LaTeX documents to spoken audio mp3 using Flask, AWS Polly, ANTLR, and SymPy

## Features
- Quickly and conveniently upload LaTeX and download mp3
- Convert .bib files along with LaTeX
- Upload and convert multiple LaTeX files at a time
- Unambiguous spoken math equations

## Contributors
Taichen Rose  
Connor Barlow  
Jacob Nameth  
Walker Herring  
Dylon Rajah  

## Dependencies
1. Python
2. Pip
3. AWS CLI

## Getting Started

1. Clone project repository
2. Go to `latex2speech` folder and run the requirements.txt page with the command `pip3 install -r requirements.txt` which installs other dependencies needed.
3. cd into tex2speech folder and run `aws configure` add in your AWS Secret Key and Access Key
4. To run project locally run `python3 -m flask run`  
