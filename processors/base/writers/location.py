# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_location(conn, location, source_id, trial_id=None):
    """Write location to database.

    Args:
        conn (dict): connection dict
        location (dict): normalized data
        source_id (str): data source id
        trial_id (str): related trial id

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False

    # Get name
    name = helpers.get_canonical_location_name(location['name'])
    if len(name) <= 1:
        return None

    # Get slug/find object
    slug = helpers.slugify_string(name)
    object = conn['database']['locations'].find_one(slug=slug)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid1().hex
        object['slug'] = slug
        create = True

    # Write object only for high priority source
    if create or source_id:  # for now do it for any source

        # Update object
        object.update({
            'source_id': source_id,
            # ---
            'name': name,
            'type': location.get('type', None),
        })

        # Write object
        conn['database']['locations'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Location - %s: %s',
            'created' if create else 'updated', name)

    return object['id']
