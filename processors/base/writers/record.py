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

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False

    # Read object
    object = readers.read_objects(conn, 'records', first=True, id=record['meta_id'])

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
            'primary_source_id': source_id,
            'source_url': record['meta_source'],
            'source_data': json.loads(json.dumps(record, cls=helpers.JSONEncoder)),
            # ---
            'primary_register': trial['primary_register'],
            'primary_id': trial['primary_id'],
            'identifiers': trial['identifiers'],
            'registration_date': trial.get('registration_date', None),
            'public_title': trial['public_title'],
            'brief_summary': trial.get('brief_summary', None),
            'scientific_title': trial.get('scientific_title', None),
            'description': trial.get('description', None),
            'recruitment_status': trial.get('recruitment_status', None),
            'eligibility_criteria': trial.get('eligibility_criteria', None),
            'target_sample_size': trial.get('target_sample_size', None),
            'first_enrollment_date': trial.get('first_enrollment_date', None),
            'study_type': trial.get('study_type', None),
            'study_design': trial.get('study_design', None),
            'study_phase': trial.get('study_phase', None),
            'primary_outcomes': trial.get('primary_outcomes', None),
            'secondary_outcomes': trial.get('primary_outcomes', None),
            'gender': trial.get('gender', None),
            'has_published_results': trial.get('has_published_results', None),
        })

        # Write object
        conn['database']['records'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Record - %s: %s',
            'created' if create else 'updated', trial['primary_id'])

    return object['id']
