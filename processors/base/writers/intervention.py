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

def write_intervention(conn, intervention, source_id):
    """Write intervention to database.

    Args:
        conn (dict): connection dict
        intervention (dict): normalized data
        source_id (str): data source id

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get name
    name = helpers.clean_string(intervention['name'])
    if len(name) <= 1:
        return None

    # Get slug/read object
    slug = helpers.slugify_string(name)
    object = readers.read_objects(conn, 'interventions', first=True, slug=slug)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['slug'] = slug
        create = True

    # Write object only for high priority source
    if create or source_id in ['icdpcs', 'fdadl']:

        # Update object
        object.update({
            'updated_at': timestamp,
            'source_id': source_id,
            # ---
            'name': name,
            'type': intervention.get('type', None),
            'description': intervention.get('description', None),
            'icdpcs_code': intervention.get('icdpcs_code', None),
            'ndc_code': intervention.get('ndc_code', None),
        })

        # Write object
        conn['database']['interventions'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Intervention - %s: %s',
            'created' if create else 'updated', name)

    return object['id']
