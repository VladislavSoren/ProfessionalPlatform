from dotenv import load_dotenv, find_dotenv
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


class Config(object):
    TESTING = False
    DEBUG = False
    # SECRET_KEY = "7ec26d07b86e8204645c637dacf21be3"
    CSRF_TRUSTED_ORIGINS = []
    CELERY_BROKER_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASS}@localhost:5672"
    EMAIL_HOST = 'localhost'


class ProductionConfig(Config):
    # DEBUG = True
    CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:1337', 'http://109.201.65.62:5666']
    DATABASES_CONFIG_DICT = \
        {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': "pg",
                'PORT': '5432',
                "TEST": {
                    "NAME": "mytestdatabase",
                },
            }
        }
    CELERY_BROKER_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASS}@rabbitmq:5672"
    EMAIL_HOST = 'mailcatcher'
    API_SEX_AGE_URL = "http://10.100.100.200:4888"
    API_EX_REC_URL = "http://10.100.100.200:4777"
    API_CAR_NUM_URL = "http://10.100.100.200:4999"


class DevelopmentConfigLocal(Config):
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
    API_SEX_AGE_URL = "http://127.0.0.1:4888"
    API_EX_REC_URL = "http://127.0.0.1:4777"
    API_CAR_NUM_URL = "http://127.0.0.1:4999"


class DevelopmentConfigDocker(Config):
    DEBUG = True
    DATABASES_CONFIG_DICT = \
        {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASSWORD,
                'HOST': "pg",
                'PORT': '5432',
                "TEST": {
                    "NAME": "mytestdatabase",
                },
            }
        }
    API_SEX_AGE_URL = "http://10.100.100.200:4888"
    API_EX_REC_URL = "http://10.100.100.200:4777"
    API_CAR_NUM_URL = "http://10.100.100.200:4999"


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


config_class_name = os.getenv("CONFIG_CLASS", "DevelopmentConfigLocal")
if config_class_name == 'ProductionConfig':
    CONFIG_OBJECT = ProductionConfig
elif config_class_name == 'DevelopmentConfigLocal':
    CONFIG_OBJECT = DevelopmentConfigLocal
elif config_class_name == 'DevelopmentConfigDocker':
    CONFIG_OBJECT = DevelopmentConfigDocker
elif config_class_name == 'TestingConfig':
    CONFIG_OBJECT = TestingConfig
else:
    CONFIG_OBJECT = DevelopmentConfigLocal
