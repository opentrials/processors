# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import adapters
from . import indexers
from . import helpsers
from . import settings
logger = logging.getLogger(__name__)


# Module API

class Mapper(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    def map_trial(adapter):

        source_id = self.index('source',
            name=adapter.table,
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name=adapter.table,
            type='register',
            data={},
        )

        for item in helpers.table_read(self.__warehouse[adapter.table]):


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = Mapper(warehouse, database)
    mapper.map_trial(adapters.Nct())
