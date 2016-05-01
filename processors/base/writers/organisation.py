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

def write_organisation(conn, organisation, trial_id=None):
    """Write organisation to database.

    Args:
        conn (object): connection object
        organisation (dict): normalized data
        trial_id (str): related trial id

    Returns:
        str: organisation identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Read
    object = readers.read_objects(conn, 'organisations', single=True,
        name=organisation['name'])

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
        'name': organisation['name'],
        'type': organisation['type'],
        'data': organisation['data'],
    })

    # Write object
    conn.database['organisations'].upsert(object, ['id'], ensure=False)

    # Write relationship
    if trial_id:
        relathionship = {
            'trial_id': trial_id,
            'organisation_id': object['id'],
            # ---
            'role': organisation['role'],
            'context': organisation['context'],
        }
        conn.database['trials_organisations'].upsert(
            relathionship, ['trial_id', 'organisation_id'], ensure=False)

    # Log
    logger.debug('Organisation - %s: %s' % (action, organisation['name']))

    return object['id']
