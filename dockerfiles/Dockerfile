FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD dockerfiles/requirements.pip /code/
RUN pip install -r requirements.pip

ADD ./src /code/src
ADD ./fileBucket /code/fileBucket

ENV PYTHONPATH /code/src/frontend
WORKDIR /code/src/frontend

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
