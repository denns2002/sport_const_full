from .base import *
from .packeges import *


DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "212.113.118.141"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        'TEST': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.yandex.ru"
EMAIL_PORT = 465
EMAIL_DOMAIN = "@yandex.ru"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(days=1)
