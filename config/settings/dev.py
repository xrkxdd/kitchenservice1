from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['kitchenservice1.onrender.com', 'localhost', '127.0.0.1', os.environ.get('RENDER_EXTERNAL_HOSTNAME')]



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
