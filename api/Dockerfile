FROM python:3.12-slim

RUN apt-get update && apt-get install git -y

WORKDIR /app

COPY pyproject.toml poetry.lock /app/


RUN pip install poetry && poetry install

COPY . /app/


ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PORT=8000 MAX_DURATION=3000

CMD poetry run gunicorn -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:$PORT