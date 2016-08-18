# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import readers
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

    # Get slug/read object
    obj = readers.read_objects(
        conn, 'documents', first=True,
        id=document['id']
    )

    # Create object
    if not obj:
        obj = {
            'id': document['id'],
        }
        create = True

    # Update object
    obj.update({
        'source_id': document.get('source_id'),
        'name': document['name'],
        'type': document['type'],
        'trial_id': document.get('trial_id'),
        'fda_approval_id': document.get('fda_approval_id'),
        'url': document['url'],
        'documentcloud_url': document.get('documentcloud_url'),
    })

    # Write object
    conn['database']['documents'].upsert(obj, ['id'], ensure=False)

    # Log debug
    logger.debug(
        'Document - %s: %s',
        'created' if create else 'updated',
        document['name'][0:50]
    )

    return obj['id']
