# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_publication(conn, publication, source_id):
    """Write publication to database.

    Args:
        conn (dict): connection dict
        publication (dict): normalized publication data
        source_id (str): data source identifier

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get slug/read object
    slug = publication['slug']
    obj = conn['database']['publications'].find_one(slug=slug)

    # Create object
    if not obj:
        obj = {
            'id': uuid.uuid1().hex,
            'created_at': timestamp,
            'slug': slug,
        }
        create = True

    # Update obj
    obj.update({
        'updated_at': timestamp,
        'source_id': source_id,
        # ---
        'source_url': publication['source_url'],
        'title': publication['title'],
        'abstract': publication['abstract'],
        'authors': publication.get('authors'),
        'journal': publication.get('journal'),
        'date': publication.get('date'),
    })

    # Validate object
    if not helpers.validate_remote_url(obj['source_url']):
        logger.warning(
            'Publication - %s wasn\'t %s because its "%s" field is invalid: %s',
            publication['title'][0:50],
            'created' if create else 'updated',
            'source_url',
            obj['source_url']
        )
        return None

    # Write obj
    conn['database']['publications'].upsert(obj, ['id'], ensure=False)

    # Log debug
    logger.debug('Publication - %s: %s',
        'created' if create else 'updated', publication['title'][0:50])

    return obj['id']
