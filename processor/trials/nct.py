# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import dataset
import sqlalchemy as sa
from collections import OrderedDict

from .. import helpers
from .. import settings


wh = dataset.connect(settings.WAREHOUSE_URL)


for item in wh['nct']:

    # Log processed item
    print('Processing: %s' % item['nct_id'])

    # Create mapping
    mapping = OrderedDict()
    mapping['nct_id'] = item['nct_id']
    mapping['euctr_id'] = None
    mapping['isrctn_id'] = None
    mapping['scientific_title'] = item['official_title']

    helpers.update_trial(
        conn=wh,
        mapping=mapping,
        identifier='isrctn::%s' % item['meta_uuid'])
