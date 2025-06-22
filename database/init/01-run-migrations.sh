#!/bin/bash
set -e

# Ensure the virtual environment is on PATH
export PATH="/opt/venv/bin:$PATH"

# Use Unix socket connection: omit host in DATABASE_URL so libpq uses PGHOST/socket
export PGHOST=/var/run/postgresql
export DATABASE_URL="postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@/$POSTGRES_DB"

echo "Starting migration process..."
echo "DATABASE_URL: $DATABASE_URL"

# Verify alembic files exist
if [ ! -f "/alembic.ini" ]; then
    echo "✗ ERROR: alembic.ini not found at /alembic.ini"
    exit 1
fi
if [ ! -d "/alembic" ]; then
    echo "✗ ERROR: alembic directory not found at /alembic"
    exit 1
fi
if [ ! -d "/alembic/versions" ] || [ -z "$(ls -A /alembic/versions 2>/dev/null)" ]; then
    echo "⚠ WARNING: No migration files in /alembic/versions. Skipping migrations."
    exit 0
fi

echo "Waiting for Postgres socket to be ready..."
# Wait until Unix socket is ready
until pg_isready -h "$PGHOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
    echo "Waiting for Postgres (socket)..."
    sleep 1
done
echo "Postgres socket is ready."

echo "Running Alembic migrations..."
# Use explicit config path
alembic -c /alembic.ini upgrade head
echo "✓ Migrations completed"
