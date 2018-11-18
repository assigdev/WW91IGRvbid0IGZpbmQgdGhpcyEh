FROM python:3.7
LABEL maintainer='assigde@gmail.com'

RUN pip install pipenv

COPY apps/dashboard/Pipfile /Pipfile
COPY apps/dashboard/Pipfile.lock /Pipfile.lock
RUN pipenv install --system

RUN mkdir -p /dashboard

RUN adduser dashboard
USER dashboard

ADD apps/dashboard/src /src
WORKDIR /dashboard/src
