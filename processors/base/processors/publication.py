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

def process_publication(conn, table, extractors):
    """Translate publication records from warehouse to database.

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

            # Extract and write publication/relationships
            publications = extractors['extract_publications'](record)
            for publication in publications:

                # Write publication
                publication_id = writers.write_publication(conn, publication, source_id)

                # Following code could be moved to separete linking processor:
                # https://github.com/opentrials/opentrials/issues/115

                # Delete existent relationships
                conn['database']['trials_publications'].delete(
                    publication_id=publication_id)

                # Write relationships
                for id in publication['trial_identifiers']:
                    trial_objects = readers.read_objects(conn, 'trials', facts=[id])
                    for trial_object in trial_objects:
                        writers.write_trial_relationship(
                            conn, 'publication', publication, publication_id, trial_id)

        except Exception as exception:
            errors += 1
            conn['database'].rollback()
            logger.exception('Processing error: %s [%s]',
                repr(exception), errors)

        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s publications from %s',
                    success, table)
