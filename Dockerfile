FROM python:3.10-alpine
LABEL MAINTAINER="Stero tECH" VERSION="1.0.0"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN /py/bin/pip install poetry && \
    /py/bin/poetry config virtualenvs.create false && \
    /py/bin/poetry install --no-dev && \
    if [ $DEV = "true" ]; \
    then /py/bin/poetry install;\
    fi &&\
    rm -rf /tmp &&\
    apk del .tmp-build-deps &&\
    adduser \
    --disabled-password \
    --no-create-home \
    stero && \
    mkdir -p /vol/web/media &&\
    mkdir -p /vol/web/static &&\
    chown -R stero:stero /vol &&\
    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER stero
