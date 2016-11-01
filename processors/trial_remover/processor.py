# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):
    """Remove trials without records.
    """

    processor = _TrialRemover(conf, conn['database'])
    processor.remove_trials_without_records()


class _TrialRemover(object):
    def __init__(self, conf, db):
        self._conf = conf
        self._db = db

    def remove_trials_without_records(self):
        """Remove trials without records.
        """

        # Prepare
        query = """
            SELECT trials.id, trials.identifiers
            FROM trials LEFT JOIN records ON records.trial_id = trials.id
            WHERE records.trial_id IS NULL AND trials.source_id != 'pubmed'
        """

        # Execute
        count = 0
        for trial in self._db.query(query):
            try:
                self._db['trials'].delete(id=trial['id'].hex)
            except Exception:
                logger.exception('Can\'t delete trial: %s', trial['identifiers'])
            else:
                logger.info('Deleted trial without records: %s', trial['identifiers'])
                count += 1
            if count and not count % 100:
                logger.info('Removed %s trials without records', count)
        logger.info('Removed %s trials without records', count)
