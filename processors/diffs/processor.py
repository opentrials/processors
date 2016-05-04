# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import datetime
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Prepare
    offset = 0
    bufsize = 10000
    query = """
        SELECT trial_id,
        array_agg(id) as record_id,
        array_agg(primary_register) as primary_register,
        array_agg(recruitment_status) as recruitment_status,
        array_agg(target_sample_size) as target_sample_size,
        array_agg(first_enrollment_date) as first_enrollment_date,
        array_agg(has_published_results) as has_published_results
        FROM trialrecords
        GROUP BY trial_id
        HAVING count(id) > 1
        ORDER BY trial_id
        LIMIT %s
        OFFSET %s
    """

    # Execute
    count = 0
    while True:
        rows = list(conn['database'].query(query % (bufsize, offset)))
        offset += bufsize
        if not rows:
            break
        for row in rows:

            # Fields list
            fields = [
                'recruitment_status',
                'target_sample_size',
                'first_enrollment_date',
                'has_published_results',
            ]

            # Get diff fields
            diff_fields = []
            def not_none(value):
                return value is not None
            for field in fields:
                if len(set(filter(not_none, row[field]))) > 1:
                    diff_fields.append(field)

            # Write diff reports
            for field in diff_fields:

                # Get values
                values = []
                items = zip(row['record_id'], row['primary_register'], row[field])
                for record_id, primary_register, value in items:
                    values.append({
                        'record_id': record_id.hex,
                        'primary_register': primary_register,
                        'value': value,
                    })

                # Update database
                timestamp = datetime.datetime.utcnow()
                conn['database']['diffs'].upsert({
                    'created_at': timestamp,
                    'updated_at': timestamp,
                    'trial_id': row['trial_id'].hex,
                    'field': field,
                    'values': json.loads(json.dumps(values, cls=base.helpers.JSONEncoder)),
                    }, ['trial_id', 'field'], ensure=False)

                # Write debug log
                count += 1
                logger.info('Diff report updated: %s/%s [%s]',
                    row['trial_id'], field, count)

                # Write info log
                if not count % 100:
                    logger.info('Diff reports added: %s', count)
