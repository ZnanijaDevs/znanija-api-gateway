FROM python:3.10.0-slim-buster
WORKDIR /code
COPY ./requirements.txt .env /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
ENV "ENV" "production"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]