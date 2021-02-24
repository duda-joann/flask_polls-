# python version
FROM python:3.9.1

#version
LABEL Version 1.0

# maintainer
MAINTAINER asiq https://github.com/duda-joann

# By default, the app uses an internal sqlite db

# main folder
WORKDIR /flask_polls

ADD requirements.txt  /flask_polls/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# set the port server to listen
EXPOSE 5000

#command to run
CMD ["python", "run.py"]