#!/bin/sh
set -e

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec python run.py
