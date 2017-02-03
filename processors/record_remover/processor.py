# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    processor = _RecordRemover(conf, conn)
    processor._remove_records_without_trial()


class _RecordRemover(object):
    def __init__(self, conf, conn):
        self._conf = conf
        self._conn = conn

    def _remove_records_without_trial(self):
        """Remove records without trial.
        """

        count = 0
        for trial in base.helpers.iter_rows(self._conn, 'database', 'trials', orderby='id'):
            try:
                # Count trials
                count += 1

                # Get all records
                records = list(self._conn['database']['records'].find(trial_id=trial['id']))

                # Trial has no multiple records
                if len(records) <= 1:
                    continue

                # Prepare identifier segments
                segments = []
                for record in records:

                    # Get set of record identifiers
                    idset = set(record['identifiers'].items())

                    # Find intersections -> update segments
                    intersection = False
                    for segment in segments:
                        if segment.intersection(idset):
                            segment.update(idset)
                            intersection = True

                    # No intersection -> new segment
                    if not intersection:
                        segments.append(idset)

                # Sort segments and get the biggest segment
                segments = list(sorted(segments, key=lambda s: len(s), reverse=True))
                biggest_segment = segments[0]

                # Delete all records without intersection with the biggest segment
                for record in records:
                    idset = set(record['identifiers'].items())
                    if not biggest_segment.intersection(idset):
                        if self._conn['database']['records'].find_one(id=record['id']):
                            self._conn['database']['records'].delete(id=record['id'])
                            logger.info('Removed record: %s', record['identifiers'])

                # Log info
                if count and not count % 100:
                    logger.info('Processed %s records', count)

            except Exception:
                base.config.SENTRY.captureException()
