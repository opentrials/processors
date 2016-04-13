# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging

from .. import helpers
from . import base
logger = logging.getLogger(__name__)


# Module API

class ContentmineTranslator(base.Translator):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    def translate(self):

        # Prepare
        trials = {}
        offset = 0
        bufsize = 10000
        query = """
            SELECT t.id, t.public_title, t.brief_summary, r.primary_id, r.scientific_title
            FROM trials as t
            JOIN trials_trialrecords as tr ON t.id = tr.trial_id
            JOIN trialrecords as r ON r.id = tr.trialrecord_id
            ORDER BY trial_id LIMIT %s OFFSET %s
        """

        # Excecute
        while True:
            rows = list(self.__database.query(query % (bufsize, offset)))
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
        print(json.dumps(trials.values(), cls=helpers.JSONEncoder, indent=4))
