FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python
ENV POETRY_VERSION=1.8.2 PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
RUN /root/.local/bin/poetry install --no-root

COPY . .
