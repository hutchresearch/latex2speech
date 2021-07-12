<div align = "center">
    <a href = "https://tex2speech-website.vercel.app/">
        <img src="/tex2speech/static/Tex2SpeechLogo.png" width="200" height="200" />
    </a>
    <h3><b>Tex2Speech</b></h3>
    <p>Sleek, easy to use text-to-speech web application for converting LaTeX documents into spoken audio.<br><a href = "https://tex2speech-website.vercel.app/docs.html"><b>Explore Tex2Speech Docs »</b></a></p>
    <a href = "https://github.com/hutchresearch/latex2speech/issues/new?template=bug_report.md">Report Bug</a> ∙ <a href = "https://github.com/hutchresearch/latex2speech/issues/new?template=feature_request.md">Request Feature</a>
</div>

### Getting Started

**To run this locally**

Note: You need to have Python on your machine and have an active Amazon Web Services account

1. Clone this repository
2. Create a virtual environment `python3 -m venv env` 
3. Activate it `source env/bin/activate`
4. From `latex2speech/tex2speech` run `pip3 install -r requirements.txt` to install all dependencies
5. Install the AWS CLI by running `pip3 install awscli` then run `aws configure` add in your AWS Secret Key and Access Key
6. Create directory called instance in the `latex2speech/tex2speech` directory
7. Create a file called config.py in the instance directory `instance/config.py`
8. Create variable in config.py called `SECRET_KEY` and assign it a random generated key (string of random characters)
9. To run project locally run `python3 application.py` 

### Documentation

Tex2Speech documentation is included in this repository under the [wiki](https://github.com/hutchresearch/latex2speech/wiki), it is also built and publicly hosted on Vercel at [https://tex2speech-website.vercel.app/](https://tex2speech-website.vercel.app/).


### Features
- Quickly and conveniently upload LaTeX and download mp3 with an intuitive web interface
- Convert .bib files along with LaTeX
- Upload and convert multiple LaTeX files at a time, as well as files zipped in .zip or .tgz files
- Wide array of supported LaTeX functions
- Unambiguous spoken math equations

### Contributing 

This project is available under the MIT license and contributions are welcomed. If you would like to contribute, please fork the repository and create a PR.
