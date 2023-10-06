FROM python:3.10-bullseye

WORKDIR /code

COPY . .

RUN pip install poetry
RUN poetry install

CMD poetry run hypercorn src/main:app -b 0.0.0.0:8000

EXPOSE 8000