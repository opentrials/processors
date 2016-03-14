# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset

from ..helpers import upsert


def map_data():


    wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
    db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


    # source

    source_id = upsert(db['sources'], ['name', 'type'], {
        'name': 'jprn',
        'type': 'register',
        'data': {},
    })


    for item in wh['jprn']:

        # Log mapping

        print('Mapped: %s' % item['unique_trial_number'])
        time.sleep(0.1)
