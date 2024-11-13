# syntax=docker/dockerfile:1.2
FROM python:3.10-slim
# put you docker configuration here

RUN apt-get update && \
    apt-get install -y build-essential gcc libssl-dev

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY challenge/ /api/challenge/
