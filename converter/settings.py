# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from dotenv import load_dotenv
load_dotenv('.env')


WAREHOUSE_URL = os.environ['OPENTRIALS_WAREHOUSE_URL']
DATABASE_URL = os.environ['OPENTRIALS_DATABASE_URL']
