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
        conn (dict): connection dict
        record (dict): raw collected data
        trial (dict): normalized data about trial
        source_id (str): related source id
        primary (bool): if record primary

    Returns:
        str: object identifier

    """
    create = False

    # Read object
    object = readers.read_objects(conn, 'trialrecords', single=True, id=record['meta_id'])

    # Create
    if not object:
        object = {}
        object['id'] = record['meta_id']
        object['created_at'] = record['meta_created']
        create = True

    # Write object only for high priority source
    if create or source_id:  # for now do it for any source

        # Update object
        object.update({
            'updated_at': record['meta_updated'],
            'trial_id': trial_id,
            'source_id': source_id,
            'source_url': record['meta_source'],
            'source_data': json.loads(json.dumps(record, cls=helpers.JSONEncoder)),
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
        conn['database']['trialrecords'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Record - %s: %s',
            'created' if create else 'updated', trial['primary_id'])

    return object['id']
