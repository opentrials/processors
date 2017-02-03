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
          ORDER BY pages DESC  -- Process files without pages first
    '''
    client = documentcloud.DocumentCloud()
    for row in conn['database'].query(query):
        pages = _get_pages(client, row['documentcloud_id'])
        if pages:
            the_file = {
                'id': row['id'].hex,
                'pages': pages,
            }
            base.writers.write_file(conn, the_file)


def _get_pages(client, doc_id):
    doc = None
    pages = None

    try:
        doc = client.documents.get(doc_id)
    except Exception as e:
        is_http_error_403 = (getattr(e, 'code', None) == 403)
        if is_http_error_403:
            raise e
        base.config.SENTRY.captureException(extra={
            'documentcloud_id': doc_id,
        })

    try:
        if doc:
            pages = [doc.get_page_text(page).strip()
                     for page in range(1, doc.pages + 1)]
            has_only_empty_pages = all([not page for page in pages])
            if has_only_empty_pages:
                pages = None
    except NotImplementedError:
        msg = 'Skipped extracting text from non-public document'
        base.config.SENTRY.captureException(message=msg, extra={
            'documentcloud_id': doc_id,
        })

    return pages
