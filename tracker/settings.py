import os
import dj_database_url
from secret import get_key, get_password, get_user

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

ROOT_URLCONF = 'tracker.urls'
LOGIN_REDIRECT_URL = '/courses/'

SECRET_KEY = get_key()
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'accounts',
    'courseperformance',
    'courses',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_tables2',
    'datetimewidget',
    'history',
    'mathfilters',
    'timer',
    'timezone_field',
    'whitenoise.runserver_nostatic',
]
WSGI_APPLICATION = 'tracker.wsgi.application'

OPTIONS = [
    'django.template.context_processors.request',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cttrackerdb',
        'USER': get_user(),
        'PASSWORD': get_password(),
        'HOST': 'localhost',
        'PORT': '',
    }
}
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))  # change database config with $DATABASE_URL

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static'), ]  # extra places for collectstatic to find static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # simplified static file serving

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'  # TODO dynamic?
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # avoid infinite redirects in Heroku
