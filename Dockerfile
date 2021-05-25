FROM alpine:latest AS base

WORKDIR /app
COPY requirements.txt /app

RUN apk add --no-cache python3 py3-pip \
    && pip3 install --upgrade pip \
    && pip3 --no-cache-dir install -r requirements.txt


FROM base AS build
WORKDIR /app
COPY . /app

EXPOSE 5000

ENV FLASK_APP api
ENV FLASK_ENV dev
ENTRYPOINT [ "flask" ]
CMD ["run", "-h", "0.0.0.0" ]
