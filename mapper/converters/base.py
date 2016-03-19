# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from six import add_metaclass
from abc import ABCMeta, abstractmethod

from .. import api
from .. import extractors
from .. import indexers
logger = logging.getLogger(__name__)


# Module API

@add_metaclass(ABCMeta)
class DirectConverter(api.Converter):

    # Public

    def __init__(self, warehouse, database, table):

        # Set attributes
        self.__warehouse = warehouse
        self.__database = database
        self.__table = table

        # Instantiate extractor
        self.__extractor = getattr(extractors, table.capitalize())()

        # Instantiate indexers
        self.__indexers = {}
        for name, value in vars(indexers).items():
            key = name.lower()
            if value is indexers.API:
                continue
            if issubclass(value, indexers.API):
                self.__indexers[key] = value(warehouse)

    def read(self):
        """Read data from warehouse.

        Args:
            table (object): datastore table object

        Yields:
            dict: the next item from table

        """
        offset = 0
        while True:
            query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
            count = self.__warehouse[self.__table].find(
                return_count=True, **query)
            if not count:
                break
            items = self.__warehouse[self.__table].find(**query)
            offset += bufsize
            for item in items:
                yield item

    def extract(self, target, item):
        """Extract data from item.

        Args:
            target (str): extractrion target
            item (dict): data item

        Returns:
            str: identifier

        """
        return self.__extractor.extract(target, item)

    def index(self, indexer, **kwargs):
        """Index item.

        Args:
            indexer (str): indexer name

        Returns:
            str: identifier

        """
        return self.__indexers[indexer].index(**kwargs)

    def write(self, table, keys, **data):
        """Write data to database.

        Args:
            table (str): table name
            keys (str[]): keys to decide insert or update
            data (dict): data to upsert

        """
        self.__database[table].upsert(data, keys, ensure=False)
