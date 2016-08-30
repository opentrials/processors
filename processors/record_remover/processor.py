# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Remove records without trial
    count = 0
    for record in base.helpers.iter_rows(conn, 'database', 'records', orderby='id'):
        trial_records = list(conn['database']['records'].find(trial_id=record['trial_id']))
        # Record not linked to others
        if len(trial_records) == 1:
            continue
        linked_identifiers = set()
        for trial_record in trial_records:
            if uuid.UUID(record['id']).hex == uuid.UUID(trial_record['id']).hex:
                continue
            linked_identifiers.update(trial_record['identifiers'].items())
        if not linked_identifiers.intersection(record['identifiers'].items()):
            conn['database']['records'].delete(id=record['id'])
            logger.info('Removed record without trials: %s', record['identifiers'])
            count += 1
        if count and not count % 100:
            logger.info('Removed %s records without trials', count)
    logger.info('Removed %s records without trials', count)
