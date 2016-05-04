# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import readers
from .. import writers
logger = logging.getLogger(__name__)


# Module API

def process_trial(conn, table, extractors):
    """Translate trial records from warehouse to database.

    Args:
        conn (dict): connection dict
        table (str): table name
        extractors (dict): extractors dict

    """

    # Extract and write source
    source = extractors['extract_source'](None)
    source_id = writers.write_source(conn, source)

    errors = 0
    success = 0
    for record in readers.read_records(conn, table):

        conn['database'].begin()

        try:

            # Extract and write trial
            trial = extractors['extract_trial'](record)
            trial_id, is_primary = writers.write_trial(conn, trial)

            # Write record
            writers.write_database_record(conn, record, source_id, trial_id, trial)

            # Write other entities
            if is_primary:

                # Delete existent relationships
                conn['database']['trials_problems'].delete(trial_id=trial_id)
                conn['database']['trials_interventions'].delete(trial_id=trial_id)
                conn['database']['trials_locations'].delete(trial_id=trial_id)
                conn['database']['trials_organisations'].delete(trial_id=trial_id)
                conn['database']['trials_persons'].delete(trial_id=trial_id)

                # Extract and write problems
                problems = extractors['extract_problems'](record)
                for problem in problems:
                    writers.write_problem(conn, problem, source_id, trial_id)

                # Extract and write interventions
                interventions = extractors['extract_interventions'](record)
                for intervention in interventions:
                    writers.write_intervention(conn, intervention, source_id, trial_id)

                # Extract and write locations
                locations = extractors['extract_locations'](record)
                for location in locations:
                    writers.write_location(conn, location, source_id, trial_id)

                # Extract and write organisations
                organisations = extractors['extract_organisations'](record)
                for organisation in organisations:
                    writers.write_organisation(conn, organisation, source_id, trial_id)

                # Extract and write persons
                persons = extractors['extract_persons'](record)
                for person in persons:
                    writers.write_person(conn, person, source_id, trial_id)

        except Exception as exception:
            errors += 1
            conn['database'].rollback()
            logger.warning('Processing error: %s [%s]',
                repr(exception), errors)
            # TODO: remove
            raise

        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s trials from %s',
                    success, table)
