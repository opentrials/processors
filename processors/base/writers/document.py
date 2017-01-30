# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from .. import helpers
from .. import config
logger = logging.getLogger(__name__)


# Module API

def write_document(conn, document):
    """Write document to database.

    Args:
        conn (dict): connection dict
        document (dict): normalized document data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    db = conn['database']
    obj = _find_document(db, document)

    # Create object
    if not obj:
        obj = {
            'id': document.get('id', uuid.uuid1().hex),
        }
        create = True

    # Update object
    obj.update({
        'source_id': document.get('source_id'),
        'document_category_id': document.get('document_category_id'),
        'name': document['name'],
        'fda_approval_id': document.get('fda_approval_id'),
        'file_id': document.get('file_id'),
        'source_url': document.get('source_url'),
    })

    # Validate object
    if obj.get('source_url') is not None and not helpers.validate_remote_url(obj['source_url']):
        logger.warning(
            'Document %s wasn\'t %s because its "%s" field is invalid: %s',
            obj['name'][0:50],
            'created' if create else 'updated',
            'source_url',
            obj['source_url']
        )
        return None

    # Write object and relationships
    try:
        db.begin()

        db['documents'].upsert(obj, ['id'], ensure=False)

        trial_id = document.get('trial_id')
        if trial_id:
            trials_documents = {
                'trial_id': trial_id,
                'document_id': obj['id'],
            }
            db['trials_documents'].insert_ignore(
                trials_documents,
                ['trial_id', 'document_id'],
                ensure=False
            )

        db.commit()
    except Exception:
        config.SENTRY.captureException(extra={
            'document': document,
        })
        db.rollback()
    else:
        # Log debug
        logger.debug(
            'Document - %s: %s',
            'created' if create else 'updated',
            document['name'][0:50]
        )
        return obj['id']


def _find_document(db, document):
    '''Finds document in DB if it exists

    If the received document has an ID, we try to find it using it. Otherwise,
    we'll look for its set of columns that must be unique. There currently are
    3 cases:

    * FDA documents - [`fda_approval_id`, `file_id`, `name`]
    * Documents with files - [`type`, `file_id`]
    * Documents with URLs - [`type`, `source_url`]
    '''
    result = None

    if document.get('id'):
        result = db['documents'].find_one(id=document['id'])
    elif document.get('fda_approval_id'):
        result = db['documents'].find_one(
            fda_approval_id=document['fda_approval_id'],
            file_id=document['file_id'],
            name=document['name']
        )
    elif document.get('file_id'):
        result = db['documents'].find_one(
            file_id=document['file_id'],
            document_category_id=document['document_category_id']
        )
    else:
        result = db['documents'].find_one(
            source_url=document['source_url'],
            document_category_id=document['document_category_id']
        )

    return result
