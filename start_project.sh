#!/bin/bash

# start all necessary containers
docker compose up -d

# wait for containers running
sleep 15

# go to project level
cd pro_platform

# install all dependencies
poetry install

# apply migrations
python manage.py migrate

# fill db prepared data
python manage.py loaddata shop_projects/fixtures/users.json
python manage.py loaddata shop_projects/fixtures/all_data.json

# start project
python manage.py runserver 0.0.0.0:5666