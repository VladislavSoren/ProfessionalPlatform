
[![Build Stat](https://github.com/VladislavSoren/ProfessionalPlatform/actions/workflows/django.yml/badge.svg?event=push)](https://github.com/VladislavSoren/ProfessionalPlatform/actions/workflows/django.yml)

# Проектная работа: `"Профессиональная платформа"`

## Фреймворк: `Django`
### Ссылка ан запущенный сервис: http://109.201.65.62:5666/ 

## Архитектура:
- Приложение `Блок аутентификации` (auth_block)
- Приложение `Магазин проектов` (shop_projects)
- Приложение `Мои проекты` (my_projects)
- БД (`PostgresSQL`) 
- Миграции
- Worker для отложенных задач (`Celery`)
- Backend для хранения и поставки отложенных задач (`RabbitMQ`)
- Сервис для отладки email рассылки (`MailCatcher`) 
- CI для автоматического тестирования проекта при `push` или `pull_request` в ветку `master` (GitHub actions)

## Проектная реализация:
- Запуск проекта осуществляется просто в терминале (запуск через `Docker` отлаживается)
- сервер для запуска `WSGIServer` (планируется перейти на nginx или gunicorn)
- `БД` запущена в `Docker` контейнере
- `Celery` запущен в `Docker` контейнере
- `RabbitMQ` запущен в `Docker` контейнере
- `MailCatcher` запущен в `Docker` контейнере

## Cтек технологий:
- Языки: `Python`, `HTML`, `CSS`
- Инструменты разработки и организации инфраструктуры: `Git`, `Github`, `Docker`, `Bash`, `PyCharm`
- Работа с БД: `PostgresSQL`, `Django ORM`
- Отложенные задачи: `Celery`, `RabbitMQ`
- Разработка API: `FastAPI`, `Uvicorn`, `Requests`
- Работа с медиа: `OpenCV`, `Pillow`
- ML: `Tensorflow`, `MXNet`, `scikit-learn`
- Тестирование: `unittest`, `Faker`, `FactoryBoy`, `Coverage.py`

## Описание функционала приложений
### Блок аутентификации:
- Возможность регистрироваться
- Возможность логиниться
- Возможность выйти из профиля
- Возможность сброса пароля через почт

### Магазин проектов:
- **User**:
    - связи:
      - 1to1 с моделью `Creator`
      - 1to∞ c моделью `Order`
      - 1to∞ c моделью `Donat`
    - отложенные задачи:
      - при сигнале `post_save` на `mailcatcher` отправляется письмо, приветствующее юзера

- **Creator**:
    - полный функционал `CRUD`
    - связи:
      - 1to1 с моделью `User`
      - 1to∞ c моделью `Project`
- **Category**:
    - полный функционал `CRUD`
    - связи:
      - 1to∞ c моделью `Project`
- **Project**:
    - полный функционал `CRUD`
    - связи:
      - ∞to1 c моделью `Creator`
      - ∞to1 c моделью `Category`
      - ∞to∞ c моделью `Order`
      - ∞to∞ c моделью `Donat`
- **Order**:
    - полный функционал `CRUD`
    - связи:
      - ∞to1 c моделью `User`
      - ∞to∞ c моделью `Project`
      - 1to1 с моделью `OrderPaymentDetails`
    - сигналы:
      - `post_save` при создании/обновлении так же создаётся/обновляется `OrderPaymentDetails`
    - отложенные задачи:
      - при сигнале `m2m_changed` на `mailcatcher` отправляется письмо с информацией о заказе и общей суммой
    - ограничения по доступу:
      - только залогинившийся пользователь имеет доступ к списку заказов
      - только юзеры уровня `staff` имеют доступ к деталям заказа
      - кнопка `archive` доступна только юзерам с разрешением `delete_order`
    - `агрегирование` в запросе (подсчёт общей суммы цен проектов в заказе)
- **OrderPaymentDetails**:
    - связи:
      - 1to1 c моделью `Order`
   - сигналы:
      - создаётся/обновляется при `post_save` для `Order`
- **Donat**:
    - полный функционал `CRUD`
    - связи:
      - ∞to1 c моделью `User`
      - ∞to∞ c моделью `Project`
    - ограничения по доступу:
      - только залогинившийся пользователь имеет доступ к списку донатов
      - только юзеры уровня `staff` имеют доступ к деталям доната
      - кнопка "archive" доступна только юзерам с разрешением `delete_donat`

### Изображение схемы БД `Магазина проектов`:
![db_schema.png](README_static/db_schema.png)

### Мои проекты:
- **sex_age_det**:
  - `try` page:
    - предсказание пола людей на изображении, загруженном юзером
    - предсказание возраста людей
    - возможность скачать подготовленное изображение для теста сервиса
    - форма ввода, включая `ImageField`
    - `ImageField` валидации: 
      - ограничение на размер загружаемого файла
    - взаимодействие с `API` сервиса `Sex-age human detection` ([Исходный код API](https://github.com/VladislavSoren/sex_age_humans_detection/blob/master/containers/sex_age_api_container/main.py))
    - вывод размеченного изображения
  - `About` page:
    - Подробная информация о сервисе `Sex-age human detection` ([Исходный код проекта](https://github.com/VladislavSoren/sex_age_humans_detection))
- **exercise_rec**:
  - `try` page:
    - классификация физических упражнений по видео, загруженном юзером (подтягивания, приседания, отжимания на брусьях)
    - подсчет количества повторений упражнения
    - возможность скачать подготовленное видео для теста сервиса
    - форма ввода, включая `FileField`
    - `FileField` валидации: 
      - ограничение на размер загружаемого файла
      - ограничение на минимальное кол-во кадров в видео
    - взаимодействие с `API` сервиса `Exercise recognition` ([Исходный код API](https://github.com/VladislavSoren/Exercise_classifier/blob/main/containers/exercise_class_api_container/main.py))
    - вывод размеченного изображения
  - `About` page:
    - Подробная информация о сервисе `Exercise recognition` ([Исходный код проекта](https://github.com/VladislavSoren/Exercise_classifier))
- **koncert_bot**:
  - `About` page:
    - Подробная информация о сервисе `Koncert bot` ([Ссылка на сервсис](https://t.me/koncert_calendar_bot))
- **car_num_det**:
  - `try` page:
    - Распознавание автомобильного номера на изображении
    - возможность скачать подготовленное изображение для теста сервиса
    - форма ввода, включая `ImageField`
    - `ImageField` валидации: 
      - ограничение на размер загружаемого файла
    - взаимодействие с `API` сервиса `Car numbers detection` ([Исходный код API](https://github.com/pavelnebel/car_numbers_detection/blob/master/containers/car_num_det_api_container/main.py))
    - вывод распознанного текста на номере и фрагмент номера, исходного изображения
  - `About` page:
    - Подробная информация о сервисе `Car numbers detection` ([Исходный код проекта](https://github.com/pavelnebel/car_numbers_detection))


## Тесты
- `auth_block` app:
  - проверяется логирование юзера

- `shop_projects` app (используется `FactoryBoy`):
  - проверяется занесение объектов моделей в БД
  - проверяется использование подходящих шаблонов
  - проверяется корректное отображение информации на страницах
  - проверяется наличие активного функционала на страницах (кнопки, ссылки и т.п.)
  - проверяются ограничения доступа к страницам
  - проверяются ограничения доступа к виджетам на страницах

- `my_projects` app
  - проверяется использование подходящих шаблонов
  - проверяется корректное отображение формы на странице `try`
  - проверяется "жив" ли `API` сервис
  - проверяется наличие корректного вывода информации на страницу, в случае успешного ответа сервиса
### Схема тестирования `my_projects` app:
![testing scheme.png](README_static%2Ftesting%20scheme.png)

### Coverage report: 92% (Coverage.py)


## Инструкция по запуску проекта
**На уровне корня**:
```shell 
poetry install
```
```shell 
docker compose up -d
```

**На уровне проекта**:
```shell 
python manage.py migrate
```
```shell 
python manage.py runserver
```
```shell 
celery -A pro_platform worker -l INFO
```

### Баш скрипты для запуска (на уровне корня):
```shell 
bash start_project.sh
```
```shell 
bash start_celery.sh
```

### Команда запуска тестов (на уровне проекта):
```shell 
python manage.py test
```
git remote add master git@gitlab.com:otus_projects/professionalplatform.git

