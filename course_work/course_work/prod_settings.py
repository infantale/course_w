from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-sdfd124f=4*pto8fy*lfr%!=o^qxx)!-1214asd1g5ejk$b(%"

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "theshop",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

STATIC_DIR = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [STATIC_DIR]
