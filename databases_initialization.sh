#!/bin/bash

set -e
set -u

function create_user_and_database() {
    local database=$1
    local username=$2
    local password=$3
    echo "Creating user '$username' and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER $username WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $username;
EOSQL
    echo "  User '$username' and database '$database' created successfully"
}

# Metadata database
create_user_and_database $AIRFLOW_METADATA_DATABASE_NAME $AIRFLOW_METADATA_DATABASE_USERNAME $AIRFLOW_METADATA_DATABASE_PASSWORD

# Celery result backend database
create_user_and_database $CELERY_BACKEND_NAME $CELERY_BACKEND_USERNAME $CELERY_BACKEND_PASSWORD

# ELT database
create_user_and_database $YOUTUBE_DATABASE_NAME $YOUTUBE_DATABASE_USERNAME $YOUTUBE_DATABASE_PASSWORD

echo "Airflow metadata, Celery backend, YouTube : databases, users and passwords created successfully"