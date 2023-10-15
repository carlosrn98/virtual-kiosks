# pull official base image
FROM python:3.11.4-slim-buster

USER root

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -m django

USER django

WORKDIR /usr/src/app
# install dependencies
RUN pip install --upgrade pip
COPY ./app/requirements.txt .
RUN pip install -r requirements.txt
