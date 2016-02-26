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


for item in wh['euctr']:

    # Log processed item
    print('Processing: %s' % item['eudract_number_with_country'])

    # Create mapping
    mapping = OrderedDict()
    mapping['isrctn_id'] = None
    mapping['euctr_id'] = item['eudract_number']
    mapping['isrctn_id'] = None
    mapping['scientific_title'] = item['full_title_of_the_trial']

    helpers.update_trial(
        conn=wh,
        mapping=mapping,
        identifier='euctr::%s' % item['meta_uuid'])
