# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim


COPY ./requirements.txt  /app/

RUN pip install -r requirements.txt

COPY ./ /app

EXPOSE 5000
