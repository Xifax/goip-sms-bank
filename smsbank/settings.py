"""
Django settings for smsbank project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Initialize secret key for production
try:
    from spec.prod.secret import SECRET_KEY
except:
    pass

# Disable debug by default
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Allowed hosts list
ALLOWED_HOSTS = [
    'localhost'
]


# Application definition

INSTALLED_APPS = (
    'smsbank.common',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'smsbank.apps.hive',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smsbank.urls'

WSGI_APPLICATION = 'smsbank.wsgi.application'


# Database
# Use sqlite by default

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Try to use production settings
try:
    from spec.prod.settings import DATABASES
except:
    pass

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'etc/static_collected')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'etc/dist'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'etc/templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'etc/uploads')

# Additional context processors
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)


# Initialize local settings
try:
    from spec.local.settings import *
except ImportError:
    pass
