FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /code

# Сначала копируем requirements.txt, для того, чтобы образ собирался быстрее (см. слои докера)
#COPY requirements.txt /code/
#RUN pip install -r requirements.txt

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

# Далее копируем сам код приложения
COPY . /code/
WORKDIR /code/

EXPOSE 8000