FROM python:3.9.23-slim-bullseye AS base

RUN adduser --create-home appuser
WORKDIR /home/appuser/app
USER appuser

COPY --chown=appuser:appuser backend/requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser backend/app ./app

EXPOSE 8080