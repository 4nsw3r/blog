FROM python:3.8-alpine

ENV PYTHONUNBUFFERED 1


WORKDIR /code

# Сначала копируем requirements.txt, для того, чтобы образ собирался быстрее (см. слои докера)
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Далее копируем сам код приложения
COPY . /code/
WORKDIR /code/

EXPOSE 8000