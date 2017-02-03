# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import config
from .. import helpers
from .. import writers
logger = logging.getLogger(__name__)


# Module API

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
            publications = extractors['extract_publications'](record)
            for publication in publications:
                writers.write_publication(conn, publication, source_id)

        except Exception:
            config.SENTRY.captureException()
            conn['database'].rollback()
        else:
            success += 1
            conn['database'].commit()
            if not success % 100:
                logger.info('Processed %s publications from %s',
                    success, table)
