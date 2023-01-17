FROM python:3.10.0-slim-buster
RUN pip install poetry

WORKDIR /code
COPY poetry.lock pyproject.toml .env /code/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --only main --no-root

COPY ./app /code/app
ENV "ENV" "production"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]