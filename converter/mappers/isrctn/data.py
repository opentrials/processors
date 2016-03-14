# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset
from dotenv import load_dotenv
load_dotenv('.env')

from ..helpers import upsert


def map_data():


    wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
    db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


    # source

    source_id = upsert(db['sources'], ['name', 'type'], {
        'name': 'isrctn',
        'type': 'register',
        'data': {},
    })


    for item in wh['isrctn']:



        # Log mapping

        print('Mapped: %s' % item['isrctn_id'])
        time.sleep(0.1)
