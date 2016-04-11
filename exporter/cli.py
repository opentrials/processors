# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import dataset
from logging.handlers import SysLogHandler

from . import settings
from .exporter import Exporter


def cli():

    # Storage
    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    # Logging
    logging.basicConfig(level=logging.INFO)
    root_logger = logging.getLogger()
    host, port = settings.LOGGING_URL.split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)

    # Exporter
    exporter = Exporter(warehouse, database)
    exporter.export(sys.argv[1])


if __name__ == '__main__':
    cli()
