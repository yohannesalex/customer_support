#!/bin/sh
# entrypoint.sh

# Navigate to the directory containing alembic.ini
cd support_assistant_backend

# Run initial migrations
alembic revision --autogenerate -m "Initial migration"

alembic -c alembic.ini upgrade head

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 9000 --reload
