FROM python:3.7
LABEL maintainer='assigde@gmail.com'

RUN pip install pipenv

COPY apps/gen_data/Pipfile /Pipfile
COPY apps/gen_data/Pipfile.lock /Pipfile.lock
RUN pipenv install --system

RUN mkdir -p /gen_data
WORKDIR /gen_data
ADD apps/gen_data/app /app

RUN adduser gen_data
USER gen_data
