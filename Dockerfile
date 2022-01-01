# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED True

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 --no-cache-dir install -r requirements.txt

COPY . .

RUN useradd -r user

USER user

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app