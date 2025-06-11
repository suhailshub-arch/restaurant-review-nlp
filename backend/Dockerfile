FROM python:3.12.11-slim-bullseye AS base

RUN adduser --disabled-password --home /home/appuser appuser
WORKDIR /home/appuser/app


COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

USER appuser

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]