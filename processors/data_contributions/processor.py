# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import logging
from .. import base
from . import extractors as extractors_module
logger = logging.getLogger(__name__)


def process(conf, conn):
    def convert_ids(contrib):
        converted_ids = {key: val.hex for key, val in contrib.items()
                        if val.__class__.__name__ == 'UUID'}
        contrib.update(converted_ids)
        return contrib

    extractors = base.helpers.get_variables(
        extractors_module, lambda x: x.startswith('extract_'))

    # Upsert source
    source = extractors['extract_source']()
    source_id = base.writers.write_source(conn, source)

    # Upsert documents from data contributions
    for_processing = """SELECT * FROM data_contributions
                        WHERE approved=true
                        AND trial_id IS NOT NULL
                        AND document_category_id IS NOT NULL
                        AND (data_url IS NOT NULL OR url IS NOT NULL);"""
    for data_contrib in conn['explorer'].query(for_processing):
        data_contrib = convert_ids(data_contrib)
        trial = conn['database']['trials'].find_one(id=data_contrib['trial_id'])
        if not trial:
            continue
        _process_document(conn, data_contrib, extractors, source_id)

    # Remove documents from data_contributions
    for_removal = """SELECT * FROM data_contributions
                     WHERE approved=false
                     AND document_id IS NOT NULL;"""
    for data_contrib in conn['explorer'].query(for_removal):
        data_contrib = convert_ids(data_contrib)
        _remove_document(conn, data_contrib)


def _process_document(conn, contrib, extractors, source_id):
    document_id = None
    document = extractors['extract_document'](contrib)
    data_request = _request_data_contribution(document['source_url'])
    if data_request:
        content_type = data_request.headers['Content-Type']

        # Check if the document is not an archive
        if not any(ctype in content_type for ctype in ['-tar', '-gtar', 'zip', '7z', 'zlib']):
            conn['database'].begin()
            try:

                # Upsert document
                doc_category = conn['database']['document_categories'].find_one(
                    id=document['document_category_id'])
                document.update({
                    'source_id': source_id,
                    'name': doc_category['name'] if doc_category else None,
                })
                document_id = base.writers.write_document(conn, document)

                # Update trial relation
                conn['database']['trials_documents'].delete(document_id=document_id)
                trial_rel = {
                    'document_id': document_id,
                    'trial_id': contrib['trial_id'],
                }
                conn['database']['trials_documents'].insert(trial_rel)

                # Update data_contribution
                contrib['document_id'] = document_id
                conn['explorer']['data_contributions'].update(contrib, ['id'])
            except Exception:
                base.config.SENTRY.captureException(extra={
                    'data_contribution_id': contrib['id'],
                })
                logger.debug('Could not process data contribution: %s', contrib['id'])
                conn['database'].rollback()
            else:
                conn['database'].commit()
                logger.info('Sucessfully processed data contribution: %s', contrib['id'])
    return document_id


def _remove_document(conn, contrib):
    conn['database'].begin()
    try:
        document_id = contrib['document_id']
        conn['database']['trials_documents'].delete(document_id=document_id)
        conn['database']['documents'].delete(id=document_id)
        contrib.update({'document_id': None})
        conn['explorer']['data_contributions'].update(contrib, ['id'])
    except Exception:
        conn['database'].rollback()
        base.config.SENTRY.captureException(extra={
            'data_contribution_id': contrib['id'],
            'document_id': document_id,
        })
        logger.debug('Could not remove contributed document: %s', document_id)
    else:
        conn['database'].commit()
        logger.info('Sucessfully removed contributed document: %s', document_id)


def _request_data_contribution(data_url):
    """Returns a Response Object or None"""
    try:
        request = requests.get(data_url)
        request.raise_for_status()
    except requests.exceptions.RequestException:
        request = None
    return request
