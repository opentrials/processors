# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from six import add_metaclass
from abc import ABCMeta

from .. import api
from .. import extractors
from ..indexers import Indexer
logger = logging.getLogger(__name__)


# Module API

@add_metaclass(ABCMeta)
class Translator(api.Translator):

    # Public

    def __init__(self, warehouse, database, extractor):

        self.__extractor = getattr(extractors, extractor.capitalize())()
        self.__indexer = Indexer(warehouse)

        if self.basis == 'warehouse':
            self.__source = warehouse
            self.__target = database
        elif self.basis == 'database':
            self.__source = database
            self.__target = warehouse
        else:
            message = 'Basis %s is not supported.'
            message = message % self.basis
            raise ValueError(message)

        if self.basis != self.__extractor.basis:
            message = 'Translator %s and extractor %s use different basises.'
            message = message % (self, self.__extractor)
            raise ValueError(message)

    def read(self):
        """Read data from warehouse.

        Yields:
            dict: the next item from table

        """
        offset = 0
        bufsize = 10
        orderby = 'meta_id'
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
            target (str): extractrion target like `trial`
            item (dict): data item

        Returns:
            str: identifier

        """
        return self.__extractor.extract(target, item)

    def index(self, target, **params):
        """Index item.

        Args:
            target (str): indexing target like `trial`
            params (dict): indexing params

        Returns:
            str: identifier

        """
        return self.__indexers.index(target, **params)

    def write(self, table, keys, **data):
        """Write data to database.

        Args:
            table (str): table name
            keys (str[]): keys to decide insert or update
            data (dict): data to upsert

        """
        self.__target[table].upsert(data, keys, ensure=False)
