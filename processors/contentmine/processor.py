# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Prepare
    trials = {}
    offset = 0
    bufsize = 10000
    query = """
        SELECT t.id, t.public_title, t.brief_summary, r.primary_id, r.scientific_title
        FROM trials as t
        JOIN trialrecords as r ON r.trial_id = t.id
        ORDER BY trial_id LIMIT %s OFFSET %s
    """

    # Excecute
    while True:
        rows = list(conn.database.query(query % (bufsize, offset)))
        if not rows:
            break
        for row in rows:
            id = row['id'].hex
            trial = trials.setdefault(id, {})
            trial['internal_id'] = id
            trial['title'] = row['public_title']
            # trial['description'] = row['brief_summary']
            terms = trial.setdefault('terms', set())
            terms.add(row['primary_id'])
            scientific_title = (row['scientific_title'] or '').strip()
            if scientific_title not in ['', 'null']:
                terms.add(scientific_title)
        offset += bufsize
        logger.info('Translated %s trial records' % offset)

    # Print
    print(json.dumps(trials.values(), cls=base.helpers.JSONEncoder, indent=4))
