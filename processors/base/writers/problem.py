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

def write_problem(conn, problem, source_id, trial_id=None):
    """Write problem to database.

    Args:
        conn (object): connection object
        problem (dict): normalized data
        trial_id (str): related trial id

    Returns:
        str: problem identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Read
    object = readers.read_objects(conn, 'problems', single=True,
        name=problem['name'])

    # Create
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        action = 'created'

    # Update
    object.update({
        'updated_at': timestamp,
        'source_id': source_id,
        # ---
        'name': problem['name'],
        'type': problem['type'],
        'data': problem['data'],
    })

    # Write object
    conn.database['problems'].upsert(object, ['id'], ensure=False)

    # Write relationship
    if trial_id:
        relathionship = {
            'trial_id': trial_id,
            'problem_id': object['id'],
            # ---
            'role': problem['role'],
            'context': problem['context'],
        }
        conn.database['trials_problems'].upsert(
            relathionship, ['trial_id', 'problem_id'], ensure=False)

    # Log
    logger.debug('Problem - %s: %s' % (action, problem['name']))

    return object['id']
