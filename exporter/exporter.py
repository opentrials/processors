# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import dataset
from . import settings


# Module API

class Exporter(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    @property
    def warehouse(self):
        """object: Warehouse dataset connection.
        """
        return self.__warehouse

    @property
    def database(self):
        """object: Database dataset connection.
        """
        return self.__database

    def export(self):
        print('export')


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    exporter = Exporter(warehouse, database)
    exporter.export()
