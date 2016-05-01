# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import dataset


# Module API

class Connection(object):

    # Public

    def __init__(self, warehouse_url, database_url):
        self._warehouse_url = warehouse_url
        self._database_url = database_url
        self._warehouse = dataset.connect(warehouse_url)
        self._database = dataset.connect(database_url)

    @property
    def warehouse(self):
        return self._warehouse

    @property
    def database(self):
        return self._database
