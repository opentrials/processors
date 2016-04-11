# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import dataset

from . import settings
from .exporter import Exporter


def cli():

    # Storage
    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    # Exporter
    exporter = Exporter(warehouse, database)
    exporter.export(sys.argv[1])


if __name__ == '__main__':
    cli()
