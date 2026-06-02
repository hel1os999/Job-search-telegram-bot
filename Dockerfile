FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY src/ ./src/

ENV PYTHONPATH=/app/src

RUN cd src && chmod +x prestart.sh

ENTRYPOINT ["src/prestart.sh"]

CMD ["python", "main.py"]
