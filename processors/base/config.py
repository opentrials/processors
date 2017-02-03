# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
import logging.config
import raven
from dotenv import load_dotenv
load_dotenv('.env')

# Environment

ENV = os.environ.get('PYTHON_ENV', 'development')
if os.environ.get('CI'):
    ENV = 'testing'

SENTRY = raven.Client(os.environ.get('SENTRY_DSN'))

# Storage

if ENV == 'testing':
    WAREHOUSE_URL = os.environ['TEST_WAREHOUSE_URL']
    DATABASE_URL = os.environ['TEST_DATABASE_URL']
else:
    WAREHOUSE_URL = os.environ['WAREHOUSE_URL']
    DATABASE_URL = os.environ['DATABASE_URL']
    EXPLORERDB_URL = os.environ['EXPLORERDB_URL']

# Logging


def setup_syslog_handler():
    if os.environ.get('LOGGING_URL', None):
        host, port = os.environ['LOGGING_URL'].split(':')
        handler = logging.handlers.SysLogHandler(address=(host, int(port)))
    else:
        handler = logging.handlers.SysLogHandler()
    return handler


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(name)s: %(message)s',
        },
    },
    'handlers': {
        'default_handler': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': 'DEBUG',
            'formatter': 'default',
        },
        'syslog_handler': {
            '()': setup_syslog_handler,
            'level': 'INFO',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['default_handler', 'syslog_handler'],
        'level': os.environ.get('LOGGING_LEVEL', 'DEBUG').upper(),
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

# OSF

OSF_URL = os.environ.get('OSF_URL', None)
OSF_KEY = os.environ.get('OSF_KEY', None)
OSF_NAMESPACE = os.environ.get('OSF_NAMESPACE', None)

# Amazon

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET', None)
AWS_S3_REGION = os.environ.get('AWS_S3_REGION', None)
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')

# DocumentCloud

DOCUMENTCLOUD_USERNAME = os.environ.get('DOCUMENTCLOUD_USERNAME')
DOCUMENTCLOUD_PASSWORD = os.environ.get('DOCUMENTCLOUD_PASSWORD')
DOCUMENTCLOUD_PROJECT = os.environ.get('DOCUMENTCLOUD_PROJECT')

# PyBossa

PYBOSSA_URL = os.environ.get('PYBOSSA_URL')
PYBOSSA_API_KEY = os.environ.get('PYBOSSA_API_KEY')
PYBOSSA_PROJECT_INDICATIONS = os.environ.get('PYBOSSA_PROJECT_INDICATIONS')

# Remove sources
REMOVE_SOURCE_IDS = os.environ.get('REMOVE_SOURCE_IDS')

# Contrib

# Contributions mapping to upload
CONTRIB = {
    # Contribution ID
    '9e4f1280-41bf-11e6-8971-f99af8d5a820': {
        # Contribution type
        'csr_synopsis': [
            # Regex to extract primary_id from filename
            r'(?P<primary_id>nct\d{3,})\.pdf',
            # Hard-coded mapping for primary_id
            ('some_document.pdf', 'ISRCT12345678'),
        ],
    },
}
