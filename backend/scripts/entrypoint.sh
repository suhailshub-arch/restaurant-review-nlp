#!/usr/bin/env bash
set -e

# Apply any pending migrations
alembic upgrade head

# Launch the app
exec uvicorn app.main:app --host 0.0.0.0 --port 8080
