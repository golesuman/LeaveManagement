FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN python -m pip install gunicorn

WORKDIR /backend-api

COPY . /backend-api/
COPY ./requirements.txt /backend-api/requirements.txt
RUN python -m pip install -r requirements.txt
CMD python manage.py migrate; python manage.py createcachetable; python manage.py runserver [::]:8000

