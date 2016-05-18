# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime
from .. import readers
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_condition(conn, condition, source_id, trial_id=None):
    """Write condition to database.

    Args:
        conn (dict): connection dict
        condition (dict): normalized data
        source_id (str): data source id
        trial_id (str): related trial id

    Returns:
        str: object identifier

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get slug/read object
    slug = helpers.slugify_string(condition['name'])
    object = readers.read_objects(conn, 'conditions', single=True, slug=slug)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['slug'] = slug
        create = True

    # Write object only for high priority source
    if create or source_id in ['icdcm']:

        # Update object
        object.update({
            'updated_at': timestamp,
            'source_id': source_id,
            # ---
            'name': condition['name'],
            'data': condition['data'],
            'description': condition['description'],
            'icdcm_code': condition['icdcm_code'],
        })

        # Write object
        conn['database']['conditions'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Condition - %s: %s',
            'created' if create else 'updated', condition['name'])

    return object['id']
