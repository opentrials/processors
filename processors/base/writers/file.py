# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
logger = logging.getLogger(__name__)


# Module API

def write_file(conn, file_data):
    """Write file to database.

    Args:
        conn (dict): connection dict
        file_data (dict): normalized file data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    obj = None
    if file_data.get('id'):
        obj = conn['database']['files'].find_one(id=file_data['id'])
    else:
        obj = conn['database']['files'].find_one(sha1=file_data['sha1'])

    if not obj:
        create = True
        obj = {
            'id': file_data.get('id', uuid.uuid1().hex),
        }

    obj.update({
        'url': file_data['url'],
        'sha1': file_data['sha1'],
        'documentcloud_id': file_data.get('documentcloud_id'),
        'text': file_data.get('text'),
    })

    conn['database']['files'].upsert(obj, ['id'], ensure=False)

    logger.debug(
        'File - %s: %s',
        'created' if create else 'updated',
        obj['id']
    )

    return obj['id']
