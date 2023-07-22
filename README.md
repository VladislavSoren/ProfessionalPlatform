# Проектная работа: "Профессиональная платформа" 

## Фреймворк: Django

## Архитектура:
- Приложение "Блок аутентификации" (auth_block)
- Приложение "Магазин проектов" (shio_projects)
- Приложение "Мои проекты" (my_projects)
- БД (PostgresSQL) 
- Миграции (alembic)
- Worker для отложенных задач (Celery)
- Backend для хранения и поставки отложенных задач (RabbitMQ)

## Проектная реализация:
- Запуск проекта осуществляется просто в терминале (запуск через Docker отлаживается)
- сервер для запуска WSGIServer (планируется перейти на nginx или gunicorn)
- БД запущена в Docker контейнере
- Celery запущен в Docker контейнере
- RabbitMQ запущен в Docker контейнере

## Описание функционала приложений
### Блок аутентификации:
- Возможность регистрироваться
- Возможность логиниться
- Возможность выйти из профиля

### Магазин проектов:
- User:
    - связи:
      - 1to1 с моделью Creator
      - 1to∞ c моделью Order
      - 1to∞ c моделью Donat
    - отложенные задачи:
      - при сигнале "post_save" на maildev отправляется письмо (НЕ реализовано)

- Creator:
    - полный функционал CRUD
    - связи:
      - 1to1 с моделью User
      - 1to∞ c моделью Project
- Category:
    - полный функционал CRUD
    - связи:
      - 1to∞ c моделью Project
- Project:
    - полный функционал CRUD
    - связи:
      - ∞to1 c моделью Creator
      - ∞to1 c моделью Category
      - ∞to∞ c моделью Order
      - ∞to∞ c моделью Donat
- Order:
    - полный функционал CRUD
    - связи:
      - ∞to1 c моделью User
      - ∞to∞ c моделью Project
      - 1to1 с моделью OrderPaymentDetails
    - сигналы:
      - "post_save" при создании/обновлении так же создаётся/обновляется OrderPaymentDetails
    - отложенные задачи:
      - при сигнале "post_save" на maildev отправляется письмо 
    - ограничения по доступу:
      - только залогинившийся пользователь имеет доступ к списку заказов
      - только юзеры уровня "staff" имеют доступ к деталям заказа
      - кнопка "archive" доступна только юзерам с разрешением "delete_order"
    - агрегирование в запросе (подсчёт общей суммы цен проектов в заказе)
- OrderPaymentDetails:
    - связи:
      - 1to1 c моделью Order
   - сигналы:
      - создаётся/обновляется при "post_save" для Order
- Donat:
    - полный функционал CRUD
    - связи:
      - ∞to1 c моделью User
      - ∞to∞ c моделью Project
    - ограничения по доступу:
      - только залогинившийся пользователь имеет доступ к списку донатов
      - только юзеры уровня "staff" имеют доступ к деталям доната
      - кнопка "archive" доступна только юзерам с разрешением "delete_donat"

### Мои проекты:



## Фотография схемы БД проекта:

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
- my_projects app