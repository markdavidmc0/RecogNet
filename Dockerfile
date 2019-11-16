# set base image
FROM python:3.7-slim-buster

# create working directory
ENV APP_HOME /recognet
ENV PORT 8000
WORKDIR $APP_HOME

# first copy and install requirements then copy app files
COPY ./requirements.txt /recognet/requirements.txt
RUN pip install -r requirements.txt
COPY ./recognet /recognet

# application execution
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 recognet.wsgi
