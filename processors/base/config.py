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
    EXPLORER_URL = os.environ['TEST_EXPLORER_URL']
else:
    WAREHOUSE_URL = os.environ['WAREHOUSE_URL']
    DATABASE_URL = os.environ['DATABASE_URL']
    EXPLORER_URL = os.environ['EXPLORER_URL']

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

# This provides aliases for document_categories in order to reduce the points of
# change. Please use these aliases throughout the code.

DOCUMENT_CATEGORIES = {
      'registry_entry': 19,
      'other': 20,
      'journal_article': 21,
      'clinical_study_report': 22,
      'clinical_study_report_synopsis': 23,
      'epar_document_section': 24,
      'fda_document_segment': 25,
      'press_release_results': 26,
      'conference_abstract_results': 27,
      'report_funder': 28,
      'case_report_form': 29,
      'grant_application': 30,
      'irb_hrec_approval': 31,
      'investigator_brochure': 32,
      'consent_form': 33,
      'statistical_analysis_plan': 34,
      'trial_protocol': 35,
      'analytics_code': 36,
      'trialist_webpage': 37,
      'lay_summary_design': 38,
      'lay_summary_results': 39,
      'individual_patient_data': 40,
      'systematic_review_data': 41,
      'blog_post': 42,
      'journal_article_critique': 43,
      'systematic_review': 44,
      'review_article': 45,
      'news_article': 46,
      'press_release_trial': 47,
      'report_from_sponsor': 48,
      'journal_article_reanalysis': 49,
}
