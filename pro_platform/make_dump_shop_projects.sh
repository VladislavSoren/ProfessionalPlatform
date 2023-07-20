#!/bin/bash

python manage.py dumpdata shop_projects > shop_projects/fixtures/all_data.json

python manage.py dumpdata auth.user  > shop_projects/fixtures/users.json
python manage.py dumpdata shop_projects.Creator > shop_projects/fixtures/creators.json

python manage.py dumpdata shop_projects.Category > shop_projects/fixtures/categories.json
python manage.py dumpdata shop_projects.Project > shop_projects/fixtures/projects.json

python manage.py dumpdata shop_projects.Order > shop_projects/fixtures/orders.json
python manage.py dumpdata shop_projects.OrderPaymentDetails > shop_projects/fixtures/orders_pay_det.json
python manage.py dumpdata shop_projects.Donat > shop_projects/fixtures/donats.json