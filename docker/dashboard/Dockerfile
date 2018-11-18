FROM python:3.7
LABEL maintainer='assigde@gmail.com'

RUN pip install pipenv

COPY apps/dashboard/Pipfile /Pipfile
COPY apps/dashboard/Pipfile.lock /Pipfile.lock
RUN pipenv install --system

RUN mkdir -p /dashboard
WORKDIR /dashboard
ADD apps/dashboard/src /src

RUN adduser dashboard
USER dashboard

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']
