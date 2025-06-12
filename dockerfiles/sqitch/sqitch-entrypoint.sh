#!/bin/bash
set -e

# Read secrets
POSTGRES_USER=$(cat /run/secrets/ocrchive_pg_user)
POSTGRES_PASSWORD=$(cat /run/secrets/ocrchive_pg_password)
POSTGRES_DB=$(cat /run/secrets/ocrchive_pg_database)

# Build the database URI
export SQITCH_TARGET="db:pg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:5432/${POSTGRES_DB}"

# Execute sqitch with the provided arguments
exec sqitch "$@"
