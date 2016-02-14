# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import dataset
import sqlalchemy as sa


warehouse = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
database = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


for record in warehouse['nct']:
    print(record)
