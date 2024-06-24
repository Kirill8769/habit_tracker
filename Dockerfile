FROM python:3.11.1

WORKDIR /app

ENV POETRY_VERSION=1.8.2 PATH='/root/.local/bin:$PATH'
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

RUN poetry lock --no-update && poetry install

COPY . .
