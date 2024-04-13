# syntax=docker/dockerfile:1
FROM python:3.12.3-slim as builder-api

WORKDIR /usr/src/api

ENV PYTHONPATH=/usr/src/api

RUN apt-get update && pip install poetry==1.8.2

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry config virtualenvs.create false  \
    && poetry install --without dev

FROM builder-api as dev-api

RUN poetry install
