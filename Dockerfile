FROM python:3.8-alpine
RUN apk --update-cache add python3-dev mariadb-dev gcc make build-base libffi-dev libressl-dev
WORKDIR /app
RUN pip install poetry