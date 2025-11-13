FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2
WORKDIR /app


RUN pip install "poetry==$POETRY_VERSION"


COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-root


COPY app ./app

COPY alembic.ini ./
COPY migrations ./migrations

CMD ["poetry", "run", "start"]
