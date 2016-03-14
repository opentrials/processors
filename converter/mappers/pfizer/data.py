# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset

from .. import helpers


def map_data():

    wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
    db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])

# source

    source_id = helpers.upsert(db['sources'], ['name', 'type'], {
        'name': 'nct',
        'type': 'register',
        'data': {},
    })


    offset = 0
    while True:  # noqa

        # Get items
        query = {'_offset': offset, '_limit': 10, 'order_by': 'meta_uuid'}
        count = wh['nct'].find(return_count=True, **query)
        if not count:
            break
        items = wh['nct'].find(**query)
        offset += 10

        for item in items:


            # Log mapping
            print('Mapped: %s' % item['nct_id'])
            time.sleep(0.1)
