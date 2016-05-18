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

def write_trial(conn, trial, source_id):
    """Write trial to database.

    Args:
        conn (dict): connection dict
        trial (dict): normilized trial data

    Returns:
        (str, bool): trial id and is primary flag

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get facts/read object
    facts = helpers.slugify_array(
        list(trial['identifiers'].values()) + [trial['scientific_title']])
    object = readers.read_objects(conn, 'trials', single=True, facts=facts)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['facts'] = []
        create = True

    # Decide primary
    is_primary = False
    priority = ['nct', 'euctr', 'isrctn']
    for register in priority:
        if 'source_id' not in object:
            is_primary = True
            break
        elif object['source_id'] == source_id:
            is_primary = True
            break
        elif source_id == register:
            is_primary = True
            break
        elif object['source_id'] == register:
            is_primary = False
            break

    # Update meta
    object.update({
        'updated_at': timestamp,
        'facts': helpers.slugify_array(object['facts'] + facts),
    })

    # Update data only if it's primary
    if is_primary:

        # Update object
        object.update({
            'source_id': source_id,
            # ---
            'primary_register': trial['primary_register'],
            'primary_id': trial['primary_id'],
            'identifiers': trial['identifiers'],
            'registration_date': trial['registration_date'],
            'public_title': trial['public_title'],
            'brief_summary': trial['brief_summary'],
            'scientific_title': trial['scientific_title'],
            'description': trial['description'],
            'recruitment_status': trial['recruitment_status'],
            'eligibility_criteria': trial['eligibility_criteria'],
            'target_sample_size': trial['target_sample_size'],
            'first_enrollment_date': trial['first_enrollment_date'],
            'study_type': trial['study_type'],
            'study_design': trial['study_design'],
            'study_phase': trial['study_phase'],
            'primary_outcomes': trial['primary_outcomes'],
            'secondary_outcomes': trial['primary_outcomes'],
            'gender': trial['gender'],
            'has_published_results': trial['has_published_results'],
        })

    # Write object
    conn['database']['trials'].upsert(object, ['id'], ensure=False)

    # Log debug
    logger.debug('Trial - %s: %s',
        'created' if create else 'updated', trial['primary_id'])

    return object['id'], is_primary
