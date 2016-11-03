"""
Django settings for thinkingweekly project on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

from os.path import abspath, dirname, join as pjoin
from django.core.exceptions import ImproperlyConfigured

# BASE_DIR should be the directory where `manage.py` is located. In our case
# it's the top of the git repo.
BASE_DIR = abspath(pjoin(dirname(__file__), '..', '..'))

PROJECT_ROOT = abspath(pjoin(dirname(__file__), '..'))

sys.path.append(pjoin(PROJECT_ROOT, 'apps'))
sys.path.append(pjoin(PROJECT_ROOT, 'libs'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_s3_storage',
    'django_extensions',
    'django_nose',

    'autoslug',
    'rest_framework',
    'widget_tweaks',
    'versatileimagefield',

    'thinkingweekly.apps.events',
    # 'thinkingweekly.apps.api',
    # 'thinkingweekly.apps.status',

    'thinkingweekly.libs.dict_get_filter',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ROOT_URLCONF = 'thinkingweekly.urls'

# https://docs.djangoproject.com/en/1.10/ref/contrib/sites/#enabling-the-sites-framework
SITE_ID = 1

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,  # TODO: reconfigure this in dev settings file
        },
    },
)

WSGI_APPLICATION = 'thinkingweekly.wsgi.application'


AUTH_PASSWORD_VALIDATORS = (
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_FORMAT = 'H:i'
DATE_FORMAT = 'l jS N Y'

# https://docs.djangoproject.com/en/1.9/ref/settings/#time-input-formats
TIME_INPUT_FORMATS = [
    '%H:%M',        # '14:30'
    '%H.%M',        # '14.30'
    '%H%M',         # '1430'
]

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MAILCHIMP_EMAIL_BEAMER = os.environ['MAILCHIMP_EMAIL_BEAMER']


if os.environ.get('USE_FILESYSTEM_STORAGE', 'false') == 'true':
    MEDIA_ROOT = abspath(pjoin(BASE_DIR, 'uploads'))
    MEDIA_URL = '/media-uploads/'

    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    FILESYSTEM_BASED_MEDIA = True  # Used in urls.py

else:
    try:
        AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
        AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
        AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME_UPLOADS']
        AWS_S3_BUCKET_NAME_STATIC = os.environ['AWS_S3_BUCKET_NAME_STATIC']

    except KeyError:
        raise ImproperlyConfigured(
            'In production mode, Django reads environment variables '
            'specifying the S3 bucket & credentials used for media uploads. '
            'Required keys are: '
            'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, '
            'AWS_S3_BUCKET_NAME_STATIC, AWS_S3_BUCKET_NAME_UPLOADS. '
            'In development, you can use local storage: '
            '`export USE_FILESYSTEM_STORAGE=true`')

    # See https://github.com/etianen/django-s3-storage

    # The region to connect to when storing files.
    AWS_REGION = "eu-west-1"

    # Uploads (media)
    DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    AWS_S3_CALLING_FORMAT = "boto.s3.connection.OrdinaryCallingFormat"
    AWS_S3_KEY_PREFIX = "uploads"
    AWS_S3_BUCKET_AUTH = True  # querystring auth
    AWS_S3_MAX_AGE_SECONDS = 10 * 60
    AWS_S3_GZIP = True
    AWS_S3_PUBLIC_URL = ""
    AWS_S3_REDUCED_REDUNDANCY = False
    AWS_S3_METADATA = {}

    # Static
    STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
    AWS_S3_CALLING_FORMAT_STATIC = "boto.s3.connection.OrdinaryCallingFormat"
    AWS_S3_BUCKET_AUTH_STATIC = False  # querystring authentication
    AWS_S3_KEY_PREFIX_STATIC = "static"
    AWS_S3_MAX_AGE_SECONDS_STATIC = 60 * 60 * 24 * 365  # 1 year.
    AWS_S3_GZIP_STATIC = True
    AWS_S3_PUBLIC_URL_STATIC = ""
    AWS_S3_REDUCED_REDUNDANCY_STATIC = False
    AWS_S3_METADATA_STATIC = {}

    FILESYSTEM_BASED_MEDIA = False  # Used in urls.py


if os.environ.get('DISABLE_OUTBOUND_EMAIL', 'false') == 'false':
    # Email
    # https://docs.djangoproject.com/en/1.9/topics/email/

    ADMINS = [('Admin', os.environ['ADMIN_EMAIL'])]

    DEFAULT_FROM_EMAIL = 'Thinking Liverpool <noreply@thinkingweekly.com>'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']


if os.environ.get('DISABLE_TWITTER', 'false') == 'false':
    TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
