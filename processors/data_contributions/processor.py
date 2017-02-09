# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import logging
from .. import base
logger = logging.getLogger(__name__)


def process(conf, conn):
    def convert_ids(contrib):
        converted_ids = {key: val.hex for key, val in contrib.items()
                        if val.__class__.__name__ == 'UUID'}
        contrib.update(converted_ids)
        return contrib

    source_id = _create_source(conn)
    for_processing = """SELECT * FROM data_contributions
                        WHERE approved=true
                        AND trial_id IS NOT NULL
                        AND data_category_id IS NOT NULL
                        AND (data_url IS NOT NULL OR url IS NOT NULL);"""

    for data_contrib in conn['explorer'].query(for_processing):
        data_contrib = convert_ids(data_contrib)
        trial = conn['database']['trials'].find_one(id=data_contrib['trial_id'])
        if not trial:
            continue
        _process_document(conn, data_contrib, source_id)

    for_removal = """SELECT * FROM data_contributions
                     WHERE approved=false
                     AND document_id IS NOT NULL;"""
    for data_contrib in conn['explorer'].query(for_removal):
        data_contrib = convert_ids(data_contrib)
        _remove_document(conn, data_contrib)


def _process_document(conn, contrib, source_id):
    document_id = None
    data_url = contrib['data_url'] or contrib['url']
    data_request = _request_data_contribution(data_url)
    if data_request:
        content_type = data_request.headers['Content-Type']

        # Check if the document is not an archive
        if not any(ctype in content_type for ctype in ['-tar', '-gtar', 'zip', '7z', 'zlib']):
            conn['database'].begin()
            try:
                # Write document_category
                category = conn['explorer']['data_categories'].find_one(id=contrib['data_category_id'])
                doc_category_id = base.writers.write_document_category(conn, category)

                # Write document
                document = {
                    'document_category_id': doc_category_id,
                    'source_url': data_url,
                    'name': category['name'],
                    'source_id': source_id,
                }
                if contrib['document_id']:
                    document.update({'id': contrib['document_id']})
                document_id = base.writers.write_document(conn, document)

                # Update trial relation
                trial_rel = {
                    'document_id': document_id,
                    'trial_id': contrib['trial_id'],
                }
                conn['database']['trials_documents'].upsert(trial_rel, ['document_id'])

                # Update data_contribution
                contrib['document_id'] = document_id
                conn['explorer']['data_contributions'].update(contrib, ['id'])
            except Exception:
                base.config.SENTRY.captureException(extra={
                    'data_contribution_id': contrib['id'],
                })
                conn['database'].rollback()
            else:
                conn['database'].commit()
                logger.info('Sucessfully processed data contribution: %s',
                            contrib['id'])

    return document_id


def _remove_document(conn, contrib):
    conn['database'].begin()
    try:
        conn['database']['trials_documents'].delete(document_id=contrib['document_id'])
        conn['database']['documents'].delete(id=contrib['document_id'])
        contrib.update({'document_id': None})
        conn['explorer']['data_contributions'].update(contrib, ['id'])
    except Exception:
        base.config.SENTRY.captureException(extra={
            'data_contribution_id': contrib['id'],
        })
        conn['database'].rollback()
    else:
        conn['database'].commit()
        logger.info('Sucessfully removed contributed document: %s',
                    contrib['document_id'])


def _request_data_contribution(data_url):
    """Returns a Response Object or None"""
    request = None
    try:
        request = requests.get(data_url)
        request.raise_for_status()
    except requests.exceptions.RequestException:
        request = None
    return request


def _create_source(conn):
    source = {
        'id': 'contrib',
        'name': 'data contribution'
    }
    return base.writers.write_source(conn, source)
