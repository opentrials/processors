# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import processors.base.helpers as helpers
import logging
logger = logging.getLogger(__name__)


def process(conf, conn):
    # Loops over each trial returning its ID and the ID of the following trial in
    # the DB. For example, if we have trials [A, B, C, D], this will return rows with
    # [[A, B], [B, C], [C, D]].
    query = """
        SELECT t1.id AS trial1_id,
               t2.id AS trial2_id
        FROM
            (SELECT id
            FROM trials
            ORDER BY id) AS t1
        -- Join with the trial in the following row
        LEFT JOIN LATERAL
            (SELECT id
            FROM trials
            WHERE id > t1.id
            ORDER BY id LIMIT 1) AS t2 ON TRUE
        -- Remove the last trial (which has no other trial to compare with)
        WHERE t2.id IS NOT NULL;
    """
    url = conf['PYBOSSA_URL']
    api_key = conf['PYBOSSA_API_KEY']
    project_id = conf['PYBOSSA_PROJECT_TRIALS_DEDUPLICATION']

    tasks_data = [_create_task(row)
                  for row in conn['database'].query(query)]

    processor = helpers.PyBossaTasksUpdater(url, api_key, project_id)
    processor.run(tasks_data, ['trial1_id', 'trial2_id'])


def _create_task(row):
    return {
        'trial1_id': row['trial1_id'].hex,
        'trial2_id': row['trial2_id'].hex,
    }
