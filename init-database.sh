#!/bin/bash
set -e

python3 check_db.py --service-name course_db --ip course_db --port 5432 

psql -h $DB_HOST -v ON_ERROR_STOP=1 -U $POSTGRES_USER  <<-EOSQL
    DROP USER IF EXISTS $DB_USER;
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
    DROP DATABASE IF EXISTS $DB_NAME;
    CREATE DATABASE $DB_NAME;
    GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
python manage.py runserver 0.0.0.0:$PORT

exec "$@"