FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD dockerfiles/requirements.pip /code/
RUN pip install -r requirements.pip

ADD ./src /code/

ENV PYTHONPATH /code/src/frontend
WORKDIR /code/src/frontend
