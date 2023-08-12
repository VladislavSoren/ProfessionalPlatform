from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

# Конфиденциальные данные
load_dotenv(find_dotenv())  # погрузка .env
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_PORT_OUT = os.getenv('DB_PORT_OUT')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASS = os.getenv('RABBIT_PASS')

# BASE_DIR = Path(__file__).resolve().parent
# DB_FILE = BASE_DIR / "app.db"

DEFAULT_DB_URL = "postgresql+psycopg2://username:passwd@0.0.0.0:9999/blog"

SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    DEFAULT_DB_URL,
)


class Config(object):
    TESTING = False
    DEBUG = False
    # SECRET_KEY = "7ec26d07b86e8204645c637dacf21be3"
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class ProductionConfig(Config):
    ...
    # SECRET_KEY = "f260e09979ef96ce87ed16afdd2dc77b"


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASES_CONFIG_DICT = \
        {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': "127.0.0.1",
                'PORT': DB_PORT_OUT,
                "TEST": {
                    "NAME": "mytestdatabase",
                },
            }
        }


class TestingConfig(Config):
    TESTING = True
    DATABASES_CONFIG_DICT = \
        {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'pro_platform',
                'USER': 'soren',
                'PASSWORD': 'pass123',
                'HOST': "postgres",
                'PORT': '5432',
                "TEST": {
                    "NAME": "mytestdatabase",
                },
            }
        }


config_class_name = os.getenv("CONFIG_CLASS", "DevelopmentConfig")
if config_class_name == 'ProductionConfig':
    CONFIG_OBJECT = ProductionConfig
elif config_class_name == 'DevelopmentConfig':
    CONFIG_OBJECT = DevelopmentConfig
elif config_class_name == 'TestingConfig':
    CONFIG_OBJECT = TestingConfig
