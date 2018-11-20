FROM python:3.7
LABEL maintainer='assigde@gmail.com'

RUN pip install pipenv

COPY apps/dashboard/Pipfile /Pipfile
COPY apps/dashboard/Pipfile.lock /Pipfile.lock
RUN pipenv install --system

ADD apps/dashboard/run_test_server.sh /run_test_server.sh
ADD apps/dashboard/celery_fix.sh /celery_fix.sh
RUN ["chmod", "+x", "/celery_fix.sh"]
RUN /celery_fix.sh

RUN mkdir -p /dashboard

RUN adduser dashboard
USER dashboard

ADD apps/dashboard/src /src
WORKDIR /dashboard/src
