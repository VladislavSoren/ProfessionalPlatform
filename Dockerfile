FROM python:3.10

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
# for cv2
RUN apt-get update
RUN apt-get install libgl1 -y
RUN apt-get install libopenblas-dev -y

# for poetry
RUN pip install --upgrade pip "poetry==1.5.1"
RUN poetry config virtualenvs.create false --local

COPY poetry.lock pyproject.toml ./

# install project dependencies
RUN poetry install --no-ansi

RUN pip install 'gunicorn==21.2.0'

# copy all not .dockerignore files in WORKDIR
COPY pro_platform .
RUN pwd
RUN ls

COPY prestart.sh .
RUN chmod +x ./prestart.sh
ENTRYPOINT ["./prestart.sh"]

CMD celery -A pro_platform worker -l INFO --detach; gunicorn pro_platform.wsgi:application --bind 0.0.0.0:8000
