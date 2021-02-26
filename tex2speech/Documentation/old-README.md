# Requirements

- AWS Account
- Python
- Flask

# Description

This is a project using Flask, decided to use Flask so I can easily communicate between HTML and Python scripts. 

app.py is the overall web page distributor, depending on certain events, this page will direct you to different pages

aws_polly_render.py is the script which will grab the .tex file and call another script which will convert it all into ssml. This script will feed it to Amazon Polly and return the presigned url 

# latex-parser
Usage: python3 latex-parser inputFileTeX outputFileSSML
