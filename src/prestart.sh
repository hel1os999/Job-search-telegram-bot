#!/usr/bin/env bash

set -e

echo "Run apply migrations.."
cd /app/src
alembic upgrade head
echo "Migrations applied!"

exec "$@"