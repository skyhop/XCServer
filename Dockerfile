FROM tiangolo/meinheld-gunicorn-flask:python2.7

RUN apt-get update
RUN apt-get install -y make libcurl4-openssl-dev
RUN pip install xcsoar flask

COPY . /app
