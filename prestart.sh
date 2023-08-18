#!/bin/bash

echo "Run migrations"
python manage.py migrate

echo "fill db prepared data"
python manage.py loaddata shop_projects/fixtures/users.json
python manage.py loaddata shop_projects/fixtures/all_data.json

exec "$@"
