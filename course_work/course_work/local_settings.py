from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-o9yxpqdxe=4*pto8fy*lfr%!=o^qxx)!-7ku7rr4oye2qz$b(%"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "shop.data",
    }
}

STATIC_URL = "/static/"
STATIC_DIR = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [STATIC_DIR]
