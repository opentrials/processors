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
from .mapper import Mapper


# Module API

def cli():

    # Storages
    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    # Logging
    logging.basicConfig(level=logging.DEBUG)
    root_logger = logging.getLogger()
    host, port = settings.LOGGING_URL.split(':')
    syslog_handler = SysLogHandler(address=(host, int(port)))
    syslog_handler.setLevel(logging.INFO)
    root_logger.addHandler(syslog_handler)

    # Mapper
    mapper = Mapper(warehouse, database)
    mapper.map(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    cli()
