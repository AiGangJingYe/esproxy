"""
Django settings for esproxy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'abcdefg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'esauth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'esproxy.urls'

WSGI_APPLICATION = 'esproxy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/login.html'


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_URL = "login.html"

ELASTICSEARCH_PROXY = "/elasticsearch"
ELASTICSEARCH_REAL = "/es"

# CAS
INSTALLED_APPS += (
    "django_cas",
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)
CAS_LOGOUT_COMPLETELY = True
CAS_IGNORE_REFERER = True
CAS_REDIRECT_URL = "/"
CAS_AUTO_CREATE_USERS = True
CAS_GATEWAY = False
CAS_RETRY_LOGIN = True
CAS_SERVER_URL = 'https://cas.corp.com'

KIBANA_DIR = '~/app/kibana'
ELASTICSEARCH_PROXY = "/elasticsearch"
ELASTICSEARCH_REAL = "/es"
AUTH_CACHE_TIMEOUT = 120

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR,'django_cache'),
    }
}

try:
    import yaml
    ELASTICSEARCH_AUTHORIZATION = {}

    for index, v in yaml.load(
        open(
            os.path.join(
                BASE_DIR, "esproxy",
                "authorization.yml"))).items():
        for action, authorizations in v.items():
            ELASTICSEARCH_AUTHORIZATION.setdefault(action, {})
            ELASTICSEARCH_AUTHORIZATION[action][index] = authorizations

except:
    ELASTICSEARCH_AUTHORIZATION = {}


try:
    from private import *
except:
    pass
