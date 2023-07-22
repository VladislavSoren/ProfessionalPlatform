# Memo for project work

https://hackmd.io/1M2zJ_2lRMe5FsT-FY3m3A

Суть проектной работы, чтобы вы разработали архитектуру приложения,
описали задачи, которые это приложение будет выполнять,
и реализовали основную функциональность.

Интернет магазин проектов (основная функциональность):
- регистрация и авторизация -
- корзина, создание
- подтверждение заказа (можно реализовать в своём проекте)
  Доп функционал:
- выставление оценок для проекта по нескольким критериям (ТЗ в miro)

API интеграции
- у меня это мои сервисы
- попробовать сделать авторизацию через GitHub

Критерии, которые повышают шанс принятия проектной работы:
- Работа с базами данных, применение различных типов связей.
- Авторизация пользователей, уровни доступа, взаимодействие пользователей (если применимо).
- взаимодействие с 3rd party сервисами, интеграции с мессенджерами / сторонними приложениями
- применение DataScience (обработка массивов данных с генерацией отчётов)
- применение других технологий, которые мы проходили на курсе


### Полезные команды:

> бращение к серверу с передачей аргументов в запросе:
http://127.0.0.1:8000/hello?name=OTUS&last_name=OCTOPUS

> Страница интерактивной документации (Swagger):
http://127.0.0.1:8000/docs

How to check if port is in use:

```shell
sudo lsof -i -P -n | grep LISTEN
```

kill the process:

```shell
kill -9 id
```

Если есть ошибка рип установке `psycopg2`:
> ERROR: Failed building wheel for psycopg2

Установи недостающие зависимости:

```shell
sudo apt-get install libpq-dev python3-dev
```

```shell
sudo apt-get install gcc
```

Get dump of app all data

```shell
python manage.py dumpdata shop_projects > shop_projects/fixtures/all_data.json
```

Get dump of particular data

```shell
python manage.py dumpdata shop_projects.Category > shop_projects/fixtures/cat-fix.json
```

Load data from dumps

```shell
python manage.py loaddata shop_projects/fixtures/cat-fix.json
```

Load users

```shell
python manage.py dumpdata auth.user  > shop_projects/fixtures/user-fix.json
```

<!--    <p class="h3 my-3">Sections:</p>-->

Questions:

- How config `static(settings.MEDIA_URL` in prod?
- Django автоматически создают тестовую БД (создаёт ли для постгрес?)