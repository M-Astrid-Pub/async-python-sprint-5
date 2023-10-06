### Run app

    poetry install

    poetry run alembic upgrade head

    poetry run hypercorn src/main:app -b 0.0.0.0:8000

or

    docker-compose up -d

serving on port 8000

### Run tests

    poetry run pytest tests

### Generate migration

    poetry run alembic revision --autogenerate -m ""

### pyproject.toml sort:

`poetry run toml-sort pyproject.toml --all --in-place`

## Run formatter
    python3 -m black .

## Run linters
    python3 -m flake8 --config setup.cfg .
    python3 -m mypy  --disallow-untyped-defs ./

