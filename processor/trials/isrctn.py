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


for item in wh['isrctn']:

    # Log processed item
    print('Processing: %s' % item['isrctn_id'])

    # Create mapping
    mapping = OrderedDict()
    mapping['nct_id'] = item['clinicaltrialsgov_number']
    mapping['euctr_id'] = None
    mapping['isrctn_id'] = item['isrctn_id']
    mapping['scientific_title'] = item['scientific_title']

    helpers.update_trial(
        conn=wh,
        mapping=mapping,
        identifier='euctr::%s' % item['meta_uuid'])
