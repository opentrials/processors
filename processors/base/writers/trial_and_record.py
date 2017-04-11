# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import uuid
import logging
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_trial_and_record(conn, trial_attrs, record_id, source_url):
    """Write trial and its record to database.

    Args:
        conn (dict): connection dict
        trial_attrs (dict): normalized trial data
        record_id (str): identifier of the record to be upserted
        source_url (str): record's source_url

    Raises:
        KeyError: if data structure is not valid

    Returns:
        (str, bool)/(None, None): trial id and is primary flag/if not written (skipped)

    """
    create = False

    trial, deduplication_method = helpers.find_trial(conn, trial_attrs, ignore_record_id=record_id)

    # Create object
    if not trial:
        trial = {
            'id': uuid.uuid1().hex,
        }
        create = True
        deduplication_method = 'initial'

    # Decide primary
    is_primary = False
    priority = ['nct', 'euctr', 'isrctn']
    if create or trial.get('source_id') == trial_attrs['source_id']:
        is_primary = True
    else:
        for register in priority:
            if trial_attrs['source_id'] == register:
                is_primary = True
                break
            elif trial.get('source_id') == register:
                is_primary = False
                break

    # BUG #389: Overwrite trials without records from the same source
    if trial.get('source_id'):
        records_count = conn['database']['records'].count(
            trial_id=trial['id'],
            source_id=trial.get('source_id')
        )
        if records_count == 0:
            is_primary = True

    # Update attributes
    trial.update(_get_all_trial_attrs(trial_attrs))

    # Write trial
    try:
        conn['database'].begin()

        if is_primary:
            conn['database']['trials'].upsert(trial, ['id'], ensure=False)

        record_id = _write_record(conn, trial, record_id, trial['source_id'], source_url, is_primary)

        _write_deduplication_log(conn, trial['id'], record_id, deduplication_method)
    except Exception:
        conn['database'].rollback()
        raise
    else:
        conn['database'].commit()

    # Log debug
    logger.debug('Trial - %s: %s',
        'created' if create else 'updated', trial_attrs['identifiers'])

    return trial['id'], is_primary


def _write_record(conn, trial, record_id, source_id=None, source_url=None, is_primary=None):
    """Write record to database.

    Args:
        conn (dict): connection dict
        trial (dict): related trial data
        record_id (dict): UUID of the record
        source_id (str): related source id (optional)
        source_url (str): Record source's URL (optional)
        is_primary (bool): is the record primary (optional)

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: record identifier/if not written (skipped)

    """
    create = False

    # Read record
    record = conn['database']['records'].find_one(id=record_id)

    # Create
    if not record:
        record = {
            'id': record_id,
        }
        create = True

    # Update record
    record.update(_get_all_trial_attrs(trial))
    record.update({
        'trial_id': trial['id'],
        'source_id': source_id or record['source_id'],
        'source_url': source_url or record['source_url'],
        'is_primary': is_primary or record.get('is_primary'),
        # ---
        'last_verification_date': trial.get('last_verification_date'),
    })

    if helpers.validate_remote_url(record['source_url']):
        try:
            conn['database'].begin()

            if record['is_primary']:
                conn['database']['records'].update(
                    {
                        'trial_id': record['trial_id'],
                        'is_primary': False,
                    },
                    ['trial_id']
                )

            conn['database']['records'].upsert(record, ['id'], ensure=False)
        except Exception:
            conn['database'].rollback()
            raise
        else:
            conn['database'].commit()

        logger.debug('Record - %s: %s',
                     'created' if create else 'updated', trial['identifiers'])

        return record['id']
    else:
        msg = "Record couldn't be written because source_url '%s' is invalid" % record['source_url']
        raise ValueError(msg)


def _write_deduplication_log(conn, trial_id, record_id, method):
    latest_log = conn['database']['trial_deduplication_logs'].find_one(
        trial_id=trial_id,
        record_id=record_id,
        order_by='-created_at'
    )

    logger.debug(
        'Trial "%s" was matched with record "%s" (method: %s)',
        trial_id,
        record_id,
        method
    )

    if not latest_log or latest_log['method'] != method:
        data = {
            'trial_id': trial_id,
            'record_id': record_id,
            'method': method,
            'commit': os.environ.get('SOURCE_COMMIT')
        }
        conn['database']['trial_deduplication_logs'].insert(data)


def _get_all_trial_attrs(trial_attrs):
    '''Returns dict with all trial attributes set from the received `trial_attrs`

    The keys of the returned dict should contain all attributes from the Trial
    table, except `id`, `created_at`, `updated_at`.
    '''
    return {
        'identifiers': trial_attrs['identifiers'],
        'public_title': trial_attrs['public_title'],
        # ---
        'source_id': trial_attrs.get('source_id'),
        'registration_date': trial_attrs.get('registration_date'),
        'completion_date': trial_attrs.get('completion_date'),
        'brief_summary': trial_attrs.get('brief_summary'),
        'scientific_title': trial_attrs.get('scientific_title'),
        'description': trial_attrs.get('description'),
        'status': trial_attrs.get('status'),
        'recruitment_status': trial_attrs.get('recruitment_status'),
        'eligibility_criteria': trial_attrs.get('eligibility_criteria'),
        'target_sample_size': trial_attrs.get('target_sample_size'),
        'first_enrollment_date': trial_attrs.get('first_enrollment_date'),
        'study_type': trial_attrs.get('study_type'),
        'study_design': trial_attrs.get('study_design'),
        'study_phase': trial_attrs.get('study_phase'),
        'primary_outcomes': trial_attrs.get('primary_outcomes'),
        'secondary_outcomes': trial_attrs.get('primary_outcomes'),
        'gender': trial_attrs.get('gender'),
        'has_published_results': trial_attrs.get('has_published_results'),
        'results_exemption_date': trial_attrs.get('results_exemption_date'),
    }
