# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import requests
import logging
import sqlalchemy
from contextlib import closing
from .. import base
from . import extractors as extractors_module
logger = logging.getLogger(__name__)


def process(conf, conn):
    def convert_ids(contribution):
        converted_ids = {key: val.hex for key, val in contribution.items()
                        if hasattr(val, 'hex')}
        contribution.update(converted_ids)
        return contribution

    extractors = base.helpers.get_variables(
        extractors_module, lambda x: x.startswith('extract_')
    )

    # Upsert source
    source = extractors['extract_source']()
    source_id = base.writers.write_source(conn, source)

    # Upsert documents from data contributions
    for_processing = '''
        SELECT * FROM data_contributions
        WHERE approved=true
        AND trial_id IS NOT NULL
        AND document_category_id IS NOT NULL
        AND (data_url IS NOT NULL OR url IS NOT NULL)
    '''
    for contribution in conn['explorer'].query(for_processing):
        base.config.SENTRY.extra_context({
            'data_contribution': contribution,
        })
        contribution = convert_ids(contribution)
        trial = conn['database']['trials'].find_one(id=contribution['trial_id'])
        if trial:
            _process_document(conn, contribution, extractors, source_id)
        else:
            msg = 'Ignoring data contribution "%s" because it refers unknown trial_id "%s"'
            logging.info(msg, contribution['id'], contribution['trial_id'])

    # Remove documents from data_contributions
    for_removal = '''
        SELECT * FROM data_contributions
        WHERE approved=false
        AND document_id IS NOT NULL
    '''
    for contribution in conn['explorer'].query(for_removal):
        base.config.SENTRY.extra_context({
            'data_contribution': contribution,
        })
        contribution = convert_ids(contribution)
        _remove_document(conn, contribution)


def _process_document(conn, contribution, extractors, source_id):
    document_id = None
    document = extractors['extract_document'](contribution)
    if _document_is_valid(document):
        conn['database'].begin()
        try:

            # Upsert document
            document_category = conn['database']['document_categories'].find_one(
                id=document['document_category_id']
            )
            document.update({
                'source_id': source_id,
                'name': document_category['name'] if document_category else None,
            })
            document_id = base.writers.write_document(conn, document)

            # Update trial relation
            conn['database']['trials_documents'].delete(document_id=document_id)
            conn['database']['trials_documents'].insert({
                'document_id': document_id,
                'trial_id': contribution['trial_id'],
            })

            # Update data_contribution
            contribution['document_id'] = document_id
            conn['explorer']['data_contributions'].update(contribution, ['id'])
        except sqlalchemy.exc.DBAPIError:
            conn['database'].rollback()
            logger.debug('Could not process data contribution: %s', contribution['id'])
            base.config.SENTRY.captureException()
        else:
            conn['database'].commit()
            logger.info('Sucessfully processed data contribution: %s', contribution['id'])
    return document_id


def _remove_document(conn, contribution):
    conn['database'].begin()
    try:
        document_id = contribution['document_id']
        conn['database']['trials_documents'].delete(document_id=document_id)
        conn['database']['documents'].delete(id=document_id)
        contribution.update({'document_id': None})
        conn['explorer']['data_contributions'].update(contribution, ['id'])
    except sqlalchemy.exc.DBAPIError:
        conn['database'].rollback()
        logger.debug('Could not remove contributed document: %s', document_id)
        base.config.SENTRY.captureException()
    else:
        conn['database'].commit()
        logger.info('Sucessfully removed contributed document: %s', document_id)


def _document_is_valid(document):
    """Returns True if document is valid, False if not"""
    is_valid = True
    contribution_headers = _get_data_contribution_headers(document['source_url'])
    archive_mimetypes = ['-tar', '-gtar', 'zip', '7z', 'zlib']
    if contribution_headers:
        content_type = contribution_headers['Content-Type']
        if any(archive_type in content_type for archive_type in archive_mimetypes):
            is_valid = False
            msg = 'Ignoring document "%s" because it is of invalid type "%s"'
            logger.info(msg, document['source_url'], content_type)
    else:
        msg = 'Ignoring document "%s" because it wasn\'t reachable.'
        logger.info(msg, document['source_url'])
        is_valid = False
    return is_valid


def _get_data_contribution_headers(data_url):
    """Returns a Response headers object or None"""
    try:
        with closing(requests.get(data_url, allow_redirects=True, stream=True)) as response:
            response.raise_for_status()
            return response.headers
    except requests.exceptions.RequestException:
        return None
