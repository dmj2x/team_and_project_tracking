FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev\
    && apk add postgresql-dev  postgresql-client\
    && pip install psycopg2 \
    && pip install pycrypto \
    && apk del build-deps

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

ADD init-database.sh /docker-entrypoint-initdb.d/init-database.sh
RUN chmod +x /docker-entrypoint-initdb.d/init-database.sh
ENTRYPOINT ["sh", "init-database.sh", "run"]