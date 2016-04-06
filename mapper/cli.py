# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import dataset

from . import settings
from .mapper import Mapper


# Module API

def cli():

    logging.basicConfig(level=logging.INFO)

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = Mapper(warehouse, database)
    mapper.map(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    cli()
