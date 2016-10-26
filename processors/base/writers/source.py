# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import datetime
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_source(conn, source):
    """Write source to database.

    Args:
        conn (dict): connection dict
        source (dict): normalized source data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Read object
    object = conn['database']['sources'].find_one(id=source['id'])

    # Create object
    if not object:
        object = {}
        object['id'] = source['id']
        object['created_at'] = timestamp
        create = True

    # Update object
    object.update({
        'updated_at': timestamp,
        # ---
        'name': source['name'],
        'type': source.get('type'),
        'source_url': source.get('source_url'),
        'terms_and_conditions_url': source.get('terms_and_conditions_url'),
    })

    # Validate object
    url_fields = ['source_url', 'terms_and_conditions_url']
    failed_url_validation = [field for field in url_fields
                             if object.get(field) is not None and not helpers.validate_remote_url(object[field])]
    if failed_url_validation:
        logger.warning(
            'Source "%s" wasn\'t %s because it has invalid fields: %s',
            object['name'],
            'created' if create else 'updated',
            {field: object[field] for field in failed_url_validation}
        )
        return None

    # Write object
    conn['database']['sources'].upsert(object, ['id'], ensure=False)

    # Log debug
    logger.debug('Source - %s: %s',
        'created' if create else 'updated', source['name'])

    return object['id']
