

## Signals:
- `post_save` signal for `OrderPaymentDetails` instance creating,
when Order is updated/created (save action)


## SharedTasks:
- send mail, when signal `post_save` from Order received 
- send mail, when signal new user is registered 


## Access restrictions
- order list not available for non-authenticated users 
- order details available only for `staff` users
- only user with permission `delete_order` can delete it
* also users without this permission cant see `Delete` button

- donat list not available for non-authenticated users
- donat details available only for `staff` users
- only user with permission `delete_donat` can delete it
* also users without this permission cant see `Delete` button


## User:
- registration page
- logging page


## Project start commands
Root level:
- `poetry install`
- `docker compose up -d`

Project level:
- `python manage.py migrate`
- `python manage.py runserver`
- `celery -A pro_platform worker -l INFO`

Alternative start:
- bash start_project.sh
- bash start_celery.sh

Tests start command on Project level:
- `python manage.py test`
### Test coverage:
- auth_block app
- shop_projects app