# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod

from .. import indexers


# Module API

@add_metaclass(ABCMeta)
class Mapper(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database
        self.__indexers = {
            'intervention': indexers.Intervention(warehouse),
            'location': indexers.Location(warehouse),
            'organisation': indexers.Organisation(warehouse),
            'person': indexers.Person(warehouse),
            'problem': indexers.Problem(warehouse),
            'source': indexers.Source(warehouse),
            'trial': indexers.Trial(warehouse),
        }

    @abstractmethod
    def map(self):
        """Map data from warehouse to database.
        """
        pass  # pragma: no cache

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
