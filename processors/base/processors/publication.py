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
        conn (object): connection object
        table (str): table name
        extractors (object): extractors set

    """

    # Extract and write source
    source = extractors.extract_source(None)
    source_id = writers.write_source(conn, source)

    errors = 0
    success = 0
    for record in readers.read_records(conn, table):

        conn['database'].begin()

        try:

            # Extract and write publication
            publication = extractors.extract_publication(record)
            writers.write_publication(conn, publication, source_id)

        except Exception as exception:
            errors += 1
            conn['database'].rollback()
            logger.warning('Processing error: %s [%s]',
                repr(exception), errors)

        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s publications from %s',
                    success, table)
