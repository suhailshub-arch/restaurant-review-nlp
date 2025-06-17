FROM python:3.9.23-slim-bullseye AS base

WORKDIR /app
COPY requirements.txt .env ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py worker.py ./
EXPOSE 8080

COPY startup.sh .
RUN chmod +x startup.sh

CMD [ "./startup.sh" ]
