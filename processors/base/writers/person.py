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

def write_person(conn, person, source_id, trial_id=None):
    """Write person to database.

    Args:
        conn (dict): connection dict
        person (dict): normalized data
        source_id (str): data source id
        trial_id (str): related trial id

    Returns:
        str: object identifier

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get slug/read object
    slug = helpers.slugify_string('{name}_{trial_id}'.format(**person))
    object = readers.read_objects(conn, 'persons', single=True, slug=slug)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['slug'] = slug
        create = True

    # Write object only for high priority source
    if create or source_id:  # for now do it for any source

        # Update object
        object.update({
            'updated_at': timestamp,
            'source_id': source_id,
            # ---
            'name': person['name'],
            'type': person['type'],
            'data': person['data'],
        })

        # Write object
        conn['database']['persons'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Person - %s: %s',
            'created' if create else 'updated', person['name'])

    return object['id']
