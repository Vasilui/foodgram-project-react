FROM python:3.8

WORKDIR /code
COPY backend/requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY backend/foodgram .

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb
RUN dpkg -i wkhtmltox_0.12.6-1.buster_amd64.deb || true

CMD gunicorn foodgram.wsgi:application --bind 0:8000