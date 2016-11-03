from .common import *

from django.core.exceptions import ImproperlyConfigured

import dj_database_url

try:
    SECRET_KEY = os.environ['SECRET_KEY']
except KeyError:
    raise ImproperlyConfigured(
        "In production mode you must specify the `SECRET_KEY` environment "
        "variable. If you're _definitely not_ running in production it's safe "
        "to set this to something insecure, eg `export SECRET_KEY=foo`")

# Set database config from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES = {'default': db_from_env}

ALLOWED_HOSTS = [
    'www.thinkingliverpool.com',
    'thinkingweekly.herokuapp.com',
    'thinkingweekly-staging.herokuapp.com',
]

LOG_DIR = '/var/log/thinkingweekly'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True,
        },
    },
}
