# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import logging
from logging.handlers import SysLogHandler
from dotenv import load_dotenv
load_dotenv('.env')


# Storage

WAREHOUSE_URL = os.environ['WAREHOUSE_URL']
DATABASE_URL = os.environ['DATABASE_URL']
EXPLORERDB_URL = os.environ['EXPLORERDB_URL']

# Logging

logging.basicConfig(level=logging.DEBUG)
if os.environ.get('LOGGING_URL', None):
    root_logger = logging.getLogger()
    host, port = os.environ['LOGGING_URL'].split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)

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
