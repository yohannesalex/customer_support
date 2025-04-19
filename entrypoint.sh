#!/bin/sh
cd support_assistant_backend

# Wait for PostgreSQL to be ready using pg_isready
while ! pg_isready -h $DB_HOST -p $DB_PORT -q; do
  sleep 1
done

# Create migrations
python -m alembic revision --autogenerate -m "Initial migration"

# Run migrations
python -m alembic upgrade head

# Start the app
exec uvicorn main:app --host 0.0.0.0 --port 9000 --reload