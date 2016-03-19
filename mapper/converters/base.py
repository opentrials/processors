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
class Converter(api.Converter):

    # Public

    def __init__(self, warehouse, database, extractor):
        if self.direct:
            self.__source = warehouse
            self.__target = database
        else:
            self.__source = database
            self.__target = warehouse
        self.__extractor = getattr(extractors, extractor.capitalize())()
        if self.direct == self.__extractor.direct:
            message = 'Converter %s and extractor %s are not compatible.'
            message = message % (self, self.__extractor)
        self.__indexer = Indexer(warehouse)

    def read(self):
        """Read data from warehouse.

        Yields:
            dict: the next item from table

        """
        offset = 0
        while True:
            query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
            count = self.__source[self.__extractor.table].find(
                return_count=True, **query)
            if not count:
                break
            items = self.__source[self.__extractor.table].find(**query)
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

    def index(self, target, **kwargs):
        """Index item.

        Args:
            indexer (str): indexer name

        Returns:
            str: identifier

        """
        return self.__indexers.index(target, **kwargs)

    def write(self, table, keys, **data):
        """Write data to database.

        Args:
            table (str): table name
            keys (str[]): keys to decide insert or update
            data (dict): data to upsert

        """
        self.__target[table].upsert(data, keys, ensure=False)
