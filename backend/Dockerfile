FROM python:3.8

WORKDIR /code
COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt
COPY foodgram .
CMD gunicorn foodgram.wsgi:application --bind 0:8000