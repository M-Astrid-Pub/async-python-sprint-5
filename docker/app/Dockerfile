FROM python:3.10-bullseye

WORKDIR /code

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main

COPY migrations .
COPY src .

RUN poetry run alembic upgrade head

CMD poetry run hypercorn src/main:app -b 0.0.0.0:8000

EXPOSE 8000