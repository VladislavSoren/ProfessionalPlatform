Client Quickstart (aiohttp)
https://docs.aiohttp.org/en/stable/client_quickstart.html

Python: FastAPI error 422 with POST
https://stackoverflow.com/questions/59929028/python-fastapi-error-422-with-post-request-when-sending-json-data

Python - convert image to JSON
https://stackoverflow.com/questions/54660800/python-convert-image-to-json

Open PIL image from byte file
https://stackoverflow.com/questions/32908639/open-pil-image-from-byte-file

Django Image Upload
https://www.javatpoint.com/django-image-upload
https://www.geeksforgeeks.org/python-uploading-images-in-django/

Django Async Model Save()
https://stackoverflow.com/questions/73268954/django-async-model-save

Django async HTTP requests with asyncio and aiohttp
https://www.youtube.com/watch?v=28KFBqi2JrA

django-async-views-examples
https://arunrocks.com/django-async-views-examples/


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
>ERROR: Failed building wheel for psycopg2

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

Questions:
- How config `static(settings.MEDIA_URL` in prod?
- Django автоматически создают тестовую БД (создаёт ли для постгрес?)