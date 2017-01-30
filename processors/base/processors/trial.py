# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import helpers
from .. import config
from .. import writers
logger = logging.getLogger(__name__)


# Module API

def process_trials(conn, table, extractors):
    """Translate trial records from warehouse to database.

    Args:
        conn (dict): connection dict
        table (str): table name
        extractors (dict): extractors dict

    """

    # Extract and write source
    source = extractors['extract_source'](None)
    source_id = writers.write_source(conn, source)

    success = 0
    for record in helpers.iter_rows(conn, 'warehouse', table, orderby='meta_id'):

        conn['database'].begin()

        try:

            # Extract and write trial
            trial = extractors['extract_trial'](record)
            trial_id, is_primary = writers.write_trial(conn, trial, source_id, record['meta_id'])
            if trial_id is None:
                continue

            # Set current primary record to false
            if is_primary:
                current_primary = conn['database']['records'].find_one(trial_id=trial_id,
                                                                       is_primary=True)
                if current_primary:
                    current_primary['is_primary'] = False
                    conn['database']['records'].update(current_primary, ['id'])

            # Write record
            writers.write_record(conn, record, source_id, trial_id, trial, is_primary)

            # Extract and write documents
            extract_documents = extractors.get('extract_documents')
            if extract_documents:

                # Extract and write document category
                doc_category = extractors.get('extract_document_category')(record)
                doc_category_id = writers.write_document_category(conn, doc_category)
                for document in extract_documents(record):
                    document.update({
                        'trial_id': trial_id,
                        'source_id': source_id,
                        'document_category_id': doc_category_id,
                    })
                    writers.write_document(conn, document)

            # Write other entities
            if is_primary:

                # Delete existent relationships
                conn['database']['trials_conditions'].delete(trial_id=trial_id)
                conn['database']['trials_interventions'].delete(trial_id=trial_id)
                conn['database']['trials_locations'].delete(trial_id=trial_id)
                conn['database']['trials_organisations'].delete(trial_id=trial_id)
                conn['database']['trials_persons'].delete(trial_id=trial_id)

                # Extract and write conditions/relationships
                conditions = extractors['extract_conditions'](record)
                for condition in conditions:
                    condition_id = writers.write_condition(conn, condition, source_id)
                    if condition_id is None:
                        continue
                    writers.write_trial_relationship(
                        conn, 'condition', condition, condition_id, trial_id)

                # Extract and write interventions/relationships
                interventions = extractors['extract_interventions'](record)
                for intervention in interventions:
                    int_id = writers.write_intervention(conn, intervention, source_id)
                    if int_id is None:
                        continue
                    writers.write_trial_relationship(
                        conn, 'intervention', intervention, int_id, trial_id)

                # Extract and write locations/relationships
                locations = extractors['extract_locations'](record)
                for location in locations:
                    location_id = writers.write_location(conn, location, source_id)
                    if location_id is None:
                        continue
                    writers.write_trial_relationship(
                        conn, 'location', location, location_id, trial_id)

                # Extract and write organisations/relationships
                organisations = extractors['extract_organisations'](record)
                for organisation in organisations:
                    org_id = writers.write_organisation(conn, organisation, source_id)
                    if org_id is None:
                        continue
                    writers.write_trial_relationship(
                        conn, 'organisation', organisation, org_id, trial_id)

                # Extract and write persons/relationships
                persons = extractors['extract_persons'](record)
                for person in persons:
                    person_id = writers.write_person(conn, person, source_id)
                    if person_id is None:
                        continue
                    writers.write_trial_relationship(
                        conn, 'person', person, person_id, trial_id)

        except Exception:
            conn['database'].rollback()
            config.SENTRY.captureException(extra={
                'record': record,
            })
        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s trials from %s',
                    success, table)
