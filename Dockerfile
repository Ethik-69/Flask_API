FROM python:3.7-alpine3.10

ADD ./ /flask_api
WORKDIR /flask_api

RUN apk add build-base
RUN apk add libffi-dev
RUN pip install --upgrade pip
RUN pip install gunicorn gevent
RUN pip install .
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

EXPOSE 8000
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=3", "--threads=2", "--log-level=debug", "run:app"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=3", "--worker-class=gevent", "--worker-connections=1000", "--preload", "--log-level=debug", "run:app"]