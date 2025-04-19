#!/bin/sh
cd support_assistant_backend

# Generate migrations
python -m alembic revision --autogenerate -m "Initial migration"

# Run migrations
python -m alembic upgrade head

# Start the app
exec uvicorn main:app --host 0.0.0.0 --port 9000 --reload