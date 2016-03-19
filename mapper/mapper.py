# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import converters
from . import settings
logger = logging.getLogger(__name__)


# Module API

class Mapper(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    def map(self, converter, extractor):
        converter = getattr(converters, converter.capitalize())(
            self.__warehouse, self.__database, extractor)
        converter.convert()


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = Mapper(warehouse, database)
    mapper.map('trial', 'nct')
