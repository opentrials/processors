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


# sources

    source_id = upsert(db['sources'], ['name', 'type'], {
        'name': 'euctr',
        'type': 'register',
        'data': {},
    })


    for item in wh['euctr']:

        # Log mapping

        print('Mapped: %s' % item['eudract_number_with_country'])
        time.sleep(0.1)
