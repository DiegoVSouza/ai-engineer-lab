#!/bin/sh
set -eu

create_role_and_database() {
  role="$1"
  password="$2"
  psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set ON_ERROR_STOP=1 --set role_name="$role" --set role_password="$password" <<'SQL'
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', :'role_name', :'role_password') \gexec
SELECT format('CREATE DATABASE %I OWNER %I', :'role_name', :'role_name') \gexec
SQL
}

create_role_and_database p04 "$P04_DB_PASSWORD"
create_role_and_database p05 "$P05_DB_PASSWORD"
create_role_and_database keycloak "$KEYCLOAK_DB_PASSWORD"

psql --username "$POSTGRES_USER" --dbname p05 --set ON_ERROR_STOP=1 \
  --command 'CREATE EXTENSION IF NOT EXISTS vector'
