# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_record(conn, record, source_id, trial_id, trial):
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
    obj = conn['database']['records'].find_one(id=record['meta_id'])

    # Create
    if not obj:
        obj = {
            'id': record['meta_id'],
            'created_at': record['meta_created'],
        }
        create = True

    # Update obj
    obj.update({
        'updated_at': record['meta_updated'],
        'trial_id': trial_id,
        'source_id': source_id,
        'source_url': record['meta_source'],
        'source_data': json.loads(json.dumps(record, cls=helpers.JSONEncoder)),
        # ---
        'identifiers': trial['identifiers'],
        'registration_date': trial.get('registration_date'),
        'completion_date': trial.get('completion_date'),
        'public_title': trial['public_title'],
        'brief_summary': trial.get('brief_summary'),
        'scientific_title': trial.get('scientific_title'),
        'description': trial.get('description'),
        'status': trial.get('status'),
        'recruitment_status': trial.get('recruitment_status'),
        'eligibility_criteria': trial.get('eligibility_criteria'),
        'target_sample_size': trial.get('target_sample_size'),
        'first_enrollment_date': trial.get('first_enrollment_date'),
        'study_type': trial.get('study_type'),
        'study_design': trial.get('study_design'),
        'study_phase': trial.get('study_phase'),
        'primary_outcomes': trial.get('primary_outcomes'),
        'secondary_outcomes': trial.get('primary_outcomes'),
        'gender': trial.get('gender'),
        'has_published_results': trial.get('has_published_results'),
        'results_exemption_date': trial.get('results_exemption_date'),
    })

    # Validate object
    if not helpers.validate_remote_url(obj['source_url']):
        logger.warning(
            'Record - %s wasn\'t %s because its "%s" field is invalid: %s',
            trial['identifiers'],
            'created' if create else 'updated',
            'source_url',
            obj['source_url']
        )
        return None

    # Write object
    conn['database']['records'].upsert(obj, ['id'], ensure=False)

    # Log debug
    logger.debug('Record - %s: %s',
        'created' if create else 'updated', trial['identifiers'])

    return obj['id']
