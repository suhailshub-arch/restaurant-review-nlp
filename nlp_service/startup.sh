#!/bin/sh
uvicorn main:app --host 0.0.0.0 --port 8080 &
python worker.py