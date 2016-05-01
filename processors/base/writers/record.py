# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from .. import readers
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_database_record(conn, record, source_id, trial_id, trial):
    """Write record to database.

    Args:
        conn (object): connection object
        record (dict): raw collected data
        trial (dict): normalized data about trial
        source_id (str): related source id
        primary (bool): if record primary

    Returns:
        str: record identifier

    """
    action = 'updated'

    # Read
    object = readers.read_objects(conn, 'trialrecords', single=True,
        id=record['meta_id'])

    # Create
    if not object:
        object = {}
        object['id'] = record['meta_id']
        object['created_at'] = record['meta_created']
        action = 'created'

    # Update
    object.update({
        'updated_at': record['meta_updated'],
        'trial_id': trial_id,
        'source_id': source_id,
        'source_url': record['meta_source'],
        'source_data': json.dumps(record, cls=helpers.JSONEncoder),
        # ---
        'primary_register': trial['primary_register'],
        'primary_id': trial['primary_id'],
        'secondary_ids': trial['secondary_ids'],
        'registration_date': trial['registration_date'],
        'public_title': trial['public_title'],
        'brief_summary': trial['brief_summary'],
        'scientific_title': trial.get('scientific_title', None),
        'description': trial.get('description', None),
        'recruitment_status': trial['recruitment_status'],
        'eligibility_criteria': trial['eligibility_criteria'],
        'target_sample_size': trial.get('target_sample_size', None),
        'first_enrollment_date': trial.get('first_enrollment_date', None),
        'study_type': trial['study_type'],
        'study_design': trial['study_design'],
        'study_phase': trial['study_phase'],
        'primary_outcomes': trial.get('primary_outcomes', None),
        'secondary_outcomes': trial.get('primary_outcomes', None),
    })

    # Write object
    conn.database['trialrecords'].upsert(object, ['id'], ensure=False)

    # Log
    logger.debug('Record - %s: %s' % (action, trial['primary_id']))

    return object['id']
