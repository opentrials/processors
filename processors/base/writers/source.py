# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime
from .. import readers
logger = logging.getLogger(__name__)


# Module API

def write_source(conn, source):
    """Write source to database.

    Args:
        conn (object): connection object
        source (dict): normalized source data

    Returns:
        str: source identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Read
    object = readers.read_objects(conn, 'sources', single=True,
        name=source['name'])

    # Create
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        action = 'created'

    # Update
    object.update({
        'updated_at': timestamp,
        # ---
        'name': source['name'],
        'type': source['type'],
        'data': source['data'],
    })

    # Write object
    conn['database']['sources'].upsert(object, ['id'], ensure=False)

    # Log
    logger.debug('Source - %s: %s' % (action, source['name']))

    return object['id']
