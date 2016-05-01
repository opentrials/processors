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

def write_intervention(conn, intervention, trial_id=None):
    """Write intervention to database.

    Args:
        conn (object): connection object
        intervention (dict): normalized data
        trial_id (str): related trial id

    Returns:
        str: intervention identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Read
    object = readers.read_objects(conn, 'interventions', single=True,
        name=intervention['name'])

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
        'name': intervention['name'],
        'type': intervention['type'],
        'data': intervention['data'],
    })

    # Write object
    conn.database['interventions'].upsert(object, ['id'], ensure=False)

    # Write relationship
    if trial_id:
        relathionship = {
            'trial_id': trial_id,
            'intervention_id': object['id'],
            # ---
            'role': intervention['role'],
            'context': intervention['context'],
        }
        conn.database['trials_interventions'].upsert(
            relathionship, ['trial_id', 'intervention_id'], ensure=False)

    # Log
    logger.debug('Intervention - %s: %s' % (action, intervention['name']))

    return object['id']
