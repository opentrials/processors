# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import documentcloud
import logging
from .. import base
logger = logging.getLogger(__name__)


def process(conf, conn):
    query = '''
        SELECT id, documentcloud_id FROM files
          WHERE documentcloud_id IS NOT NULL
    '''
    client = _documentcloud_client(conf)
    for row in conn['database'].query(query):
        text = _get_text(client, row['documentcloud_id'])
        if text:
            the_file = {
                'id': row['id'].hex,
                'text': text,
            }
            base.writers.write_file(conn, the_file)


def _get_text(client, doc_id):
    doc = None
    text = None

    try:
        doc = client.documents.get(doc_id)
    except Exception as e:
        is_http_error_403 = (getattr(e, 'code', None) == 403)
        if is_http_error_403:
            raise e
        msg = 'Exception when loading document %s: %s' % (doc_id, e.message)
        logger.warn(msg)

    try:
        if doc:
            text = doc.get_full_text()
    except NotImplementedError:
        msg = 'Skipped extracting text from non-public document "%s"' % doc_id
        logger.debug(msg)

    return text


def _documentcloud_client(conf):
    username = conf['DOCUMENTCLOUD_USERNAME']
    password = conf['DOCUMENTCLOUD_PASSWORD']

    return documentcloud.DocumentCloud(username, password)
