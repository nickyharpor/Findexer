# syntax=docker/dockerfile:1

FROM python:3.10.0-bullseye
WORKDIR /usr/src/app
COPY . .
RUN pip3 install -r requirements.txt
ENV FLASK_APP app.py
