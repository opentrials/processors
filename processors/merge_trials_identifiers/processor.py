# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):
    """Merge trial identifiers
    """

    # Prepare
    query = """
        WITH records_identifiers AS (
            SELECT trial_id, ids.key, ids.value
            FROM records, jsonb_each(identifiers) AS ids
        ), merged_identifiers AS (
            SELECT trials.id,
                trials.identifiers AS trial_identifiers,
                json_object_agg(key, value)::jsonb AS records_identifiers
            FROM records_identifiers
            INNER JOIN trials ON records_identifiers.trial_id = trials.id
            GROUP BY trials.id
        )
        SELECT *
        FROM merged_identifiers
        WHERE trial_identifiers != records_identifiers
    """

    # Execute
    count = 0
    failed = 0

    for result in conn['database'].query(query):
        try:
            trial_identifiers = result['trial_identifiers']
            identifiers = dict(trial_identifiers.items() +
                               result['records_identifiers'].items())

            if sorted(identifiers.items()) == sorted(trial_identifiers.items()):
                continue

            trial = {
                'id': result['id'].hex,
                'identifiers': identifiers,
                'updated_at': datetime.datetime.utcnow(),
            }

            conn['database']['trials'].update(trial, ['id'])
            count += 1
            logger.info("[{}] Trial {} was updated".format(count, trial['id']))

        except Exception:
            base.config.SENTRY.captureException(extra={
                'identifiers': result['trial_identifiers'],
            })
            failed += 1

    logger.info('{} trials updated'.format(count))
    logger.info('{} trials failed'.format(failed))
