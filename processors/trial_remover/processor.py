# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Remove trials without records
    count = 0
    query = """
        SELECT trials.id, trials.identifiers
        FROM trials LEFT JOIN records ON records.trial_id = trials.id
        WHERE records.trial_id IS NULL AND trials.source_id != 'pubmed'
    """
    for trial in conn['database'].query(query):
        try:
            conn['database']['trials'].delete(id=trial['id'].hex)
        except Exception:
            logger.exception('Can\'t delete trial: %s', trial['identifiers'])
        else:
            logger.info('Deleted trial without records: %s', trial['identifiers'])
            count += 1
        if count and not count % 100:
            logger.info('Removed %s trials without records', count)
    logger.info('Removed %s trials without records', count)
