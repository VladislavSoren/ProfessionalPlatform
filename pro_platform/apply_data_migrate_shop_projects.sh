#!/bin/bash

python manage.py loaddata shop_projects/fixtures/users.json
python manage.py loaddata shop_projects/fixtures/creators.json

python manage.py loaddata shop_projects/fixtures/categories.json
python manage.py loaddata shop_projects/fixtures/projects.json

python manage.py loaddata shop_projects/fixtures/orders.json
python manage.py loaddata shop_projects/fixtures/orders_pay_det.json
python manage.py loaddata shop_projects/fixtures/donats.json