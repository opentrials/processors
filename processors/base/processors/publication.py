# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import helpers
from .. import writers
logger = logging.getLogger(__name__)


def process_publications(conn, table, extractors):
    """Translate publication records from warehouse to database.

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

            # Extract and write publications
            publication = extractors['extract_publication'](record)
            publication_id = writers.write_publication(conn, publication, source_id)

            # Delete existent relationships
            conn['database']['trials_publications'].delete(publication_id=publication_id)

            # Create new relationships
            for identifiers in publication.get('identifiers'):
                trial = helpers.find_trial_by_identifiers(conn, identifiers=identifiers)
                if trial:
                    writers.write_trial_relationship(
                        conn, 'publication', publication, publication_id, trial['id']
                    )
                    logger.debug('Linked %s to "%s"',
                        trial['identifiers'].values(), publication['title'][0:50]
                    )
        except Exception:
            conn['database'].rollback()
            logger.debug('Couldn\'t process publication from record: %s',
                record['meta_id']
            )
            raise
        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s publications from %s', success, table)
