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

def write_location(conn, location, trial_id=None):
    """Write location to database.

    Args:
        conn (object): connection object
        location (dict): normalized data
        trial_id (str): related trial id

    Returns:
        str: location identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Read
    object = readers.read_objects(conn, 'locations', single=True,
        name=location['name'])

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
        'name': location['name'],
        'type': location['type'],
        'data': location['data'],
    })

    # Write object
    conn.database['locations'].upsert(object, ['id'], ensure=False)

    # Write relationship
    if trial_id:
        relathionship = {
            'trial_id': trial_id,
            'location_id': object['id'],
            # ---
            'role': location['role'],
            'context': location['context'],
        }
        conn.database['trials_locations'].upsert(
            relathionship, ['trial_id', 'location_id'], ensure=False)

    # Log
    logger.debug('Location - %s: %s' % (action, location['name']))

    return object['id']
