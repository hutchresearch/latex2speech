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
Jacob Nemeth  
Walker Herring  
Dylon Rajah  

## Dependencies
1. Python
2. Pip
3. AWS CLI
4. AWS Account

## Getting Started

1. Clone project repository
2. Go to `latex2speech` folder and run the requirements.txt page with the command `pip3 install -r requirements.txt` which installs other dependencies needed.
3. cd into tex2speech folder and run `aws configure` add in your AWS Secret Key and Access Key
4. Create directory called instance in the latex2speech directory (Keep the instance directory and everything in it private do not share)
5. Create a file called config.py in the instance directory
6. Create variable in config.py called `SECRET_KEY` and assign it a random generated key (string of random characters)
7. To run project locally run `python3 -m flask run`  
