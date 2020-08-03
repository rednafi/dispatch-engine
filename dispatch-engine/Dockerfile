# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./requirements.txt  /app/

RUN pip install -r requirements.txt

COPY ./ /app

EXPOSE 5000
