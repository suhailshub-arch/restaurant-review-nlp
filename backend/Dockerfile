FROM python:3.12.11-slim-bullseye AS base

RUN adduser --disabled-password --home /home/appuser appuser
WORKDIR /home/appuser/app


COPY requirements.txt .
# trunk-ignore(hadolint/DL3013)
# trunk-ignore(hadolint/DL3042)
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

USER appuser

EXPOSE 8080

# trunk-ignore(hadolint/DL3025)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]