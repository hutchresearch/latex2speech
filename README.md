# TeX2Speech
A web application for converting LaTeX documents to spoken audio. You can demo the program [here](http://tex2speech.eba-mgbfwtgw.us-east-1.elasticbeanstalk.com/).

## Features
- Quickly and conveniently upload LaTeX and download mp3
- Convert .bib files along with LaTeX
- Upload and convert multiple LaTeX files at a time
- Unambiguous spoken math equations

## Contributors
Connor Barlow
Walker Herring
Jacob Nemeth
Dylon Rajah
Taichen Rose   

## Dependencies
1. Python
2. Pip
3. AWS CLI
4. AWS Account

## Getting Started

**To run this locally**
1. Clone project repository
2. Create a virtual environment `python3 -m venv env` then run your virtual enviornment `source env/bin/activiate`
3. Go to `latex2speech/tex2speech` folder and run the requirements.txt page with the command `pip3 install -r requirements.txt` which installs other dependencies needed.
4. Then run `aws configure` add in your AWS Secret Key and Access Key
5. Create directory called instance in the `latex2speech/tex2speech` directory (Keep the instance directory and everything in it private do not share)
5. Create a file called config.py in the instance directory `instance/config.py`
7. Create variable in config.py called `SECRET_KEY` and assign it a random generated key (string of random characters)
8. To run project locally run `python3 application.py`  
