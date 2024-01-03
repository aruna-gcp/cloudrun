FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
