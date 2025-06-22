#!/bin/bash
set -e

export PATH="/opt/venv/bin:$PATH"
# Make sure Python searches root
export PYTHONPATH="/:$PYTHONPATH"
export PGHOST=/var/run/postgresql
export DATABASE_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@/$POSTGRES_DB"

echo "Starting data load process..."
echo "PYTHONPATH: $PYTHONPATH"

echo "Waiting for Postgres socket..."
until pg_isready -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for Postgres (socket)..."
  sleep 1
done
echo "Postgres socket ready."

cd /docker-entrypoint-initdb.d
echo "Contents of /shared:"
ls -l /shared || echo "/shared not found"
echo "Contents of /:"
ls -l / | head -n 20

echo "Running data loading script..."
python3 load_init_data.py
echo "✓ Data loading completed"
