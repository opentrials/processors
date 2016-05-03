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

def write_publication(conn, publication, source_id):
    """Write publication to database.

    Args:
        conn (object): connection object
        publication (dict): normalized publication data
        source_id (str): data source identifier

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Get slug/facts
    slug = helpers.slugify_string(publication['source_url'])

    # Read
    object = readers.read_objects(conn, 'publications', single=True,
        slug=slug)

    # Create
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['slug'] = slug
        action = 'created'

    # Update
    object.update({
        'updated_at': timestamp,
        'source_id': source_id,
        # ---
        'source_url': publication['source_url'],
        'title': publication['title'],
        'abstract': publication['abstract'],
        'authors': publication['authors'],
        'journal': publication['journal'],
        'date': publication['date'],
    })

    # Write object
    conn['database']['publications'].upsert(object, ['id'], ensure=False)

    # Write relationship
    for identifier in publication['identifiers']:
        trial_objects = readers.read_objects(conn, 'trials',
            facts=[identifier])
        for trial_object in trial_objects:
            relathionship = {
                'trial_id': trial_object['id'],
                'publication_id': object['id'],
                # ---
            }
            conn['database']['trials_publications'].upsert(
                relathionship, ['trial_id', 'publication_id'], ensure=False)

    # Log
    logger.debug('Publication - %s: %s' % (action, publication['title'][0:50]))

    return object['id']
