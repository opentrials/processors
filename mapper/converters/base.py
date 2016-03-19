# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from six import add_metaclass
from abc import ABCMeta, abstractmethod

from .. import api
logger = logging.getLogger(__name__)


# Module API

@add_metaclass(ABCMeta)
class DirectConverter(api.Converter):

    # Public

    def __init__(self, warehouse, database):

        # Set attributes
        self.__warehouse = warehouse
        self.__database = database
        self.__extractors = {}
        self.__indexers = {}

        # Instantiate extractors
        for name, value in vars(extractors).items():
            key = name.lower()
            if issubclass(value, extractors.API):
                self.__extractors[key] = value()

        # Instantiate indexers
        for name, value in vars(indexers).items():
            key = name.lower()
            if issubclass(value, indexers.API):
                self.__indexers[key] = value(warehouse)

    def read(self, table):
        """Read data from warehouse.

        Args:
            table (object): datastore table object

        Yields:
            dict: the next item from table

        """
        offset = 0
        while True:
            query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
            count = self.__warehouse[table].find(return_count=True, **query)
            if not count:
                break
            items = self.__warehouse[table].find(**query)
            offset += bufsize
            for item in items:
                yield item

    def extract(self, extractor, target, item):
        """Extract data from item.

        Args:
            extractor (str): extractor name
            target (str): extractrion target

        Returns:
            str: identifier

        """
        return self.__extractors[extractor].extract(target, item)

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
