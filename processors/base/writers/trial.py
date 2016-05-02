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

def write_trial(conn, trial):
    """Write trial to database.

    Args:
        conn (object): connection object
        trial (dict): normilized trial data

    Returns:
        (str, bool): trial id and is primary flag

    """
    action = 'updated'
    timestamp = datetime.datetime.utcnow()

    # Get slug/facts
    facts = helpers.slugify_array(trial['identifiers'] + [trial['scientific_title']])

    # Read
    object = readers.read_objects(conn, 'trials', single=True,
        facts=facts)

    # Create
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['facts'] = []
        action = 'created'

    # Decide primary
    is_primary = False
    priority = ['nct', 'euctr', 'isrctn']
    for register in priority:
        if 'primary_register' not in object:
            is_primary = True
            break
        elif object['primary_register'] == trial['primary_register']:
            is_primary = True
            break
        elif trial['primary_register'] == register:
            is_primary = True
            break
        elif object['primary_register'] == register:
            break

    # Update
    object.update({
        'updated_at': timestamp,
        'facts': helpers.slugify_array(object['facts'] + facts),
    })
    if is_primary:
        object.update({
            # ---
            'primary_register': trial['primary_register'],
            'primary_id': trial['primary_id'],
            'secondary_ids': trial['secondary_ids'],
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
    conn.database['trials'].upsert(object, ['id'], ensure=False)

    # Log
    logger.debug('Trial - %s: %s' % (action, trial['primary_id']))

    return object['id'], is_primary
