FROM python:3.10.6-slim-buster

WORKDIR /app
RUN mkdir /app/data

RUN pip3 install requests flask

COPY jenkins/fetcher.py /app

CMD [ "python3", "/app/fetcher.py" ]