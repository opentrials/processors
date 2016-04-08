# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging

logger = logging.getLogger(__name__)


# Module API

class Pipeline(object):
    """Pipeline representation (e.g. warehouse to database).

    Args:
        source (object): datastore connection
        target (object): datastore connection

    """

    # Public

    def __init__(self, source, target):
        self.__source = source
        self.__target = target

    def read(self, table, bufsize=100, orderby='meta_id'):
        """Read data from source.

        Yields:
            dict: the next item from table

        """
        offset = 0
        while True:
            query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
            count = self.__source[table].find(return_count=True, **query)
            if not count:
                break
            items = self.__source[table].find(**query)
            offset += bufsize
            for item in items:
                item['meta_id'] = uuid.UUID(item['meta_id']).hex
                yield item

    def begin(self):
        """Begin transaction on target.
        """
        self.__target.begin()

    def delete(self, table, **filter):
        """Delete from target.

        Args:
            table (str): table name
            filter (dict): deletion filter

        """
        self.__target[table].delete(**filter)

    def update(self, table, keys, **data):
        """Update target.

        Args:
            table (str): table name
            keys (str[]): filter keys
            data (dict): data to upsert

        """
        self.__target[table].update(data, keys, ensure=False)

    def write_entity(self, table, entity, **data):
        """Write entity to target.

        Args:
            table (str): table name
            entity (dict): base data entry
            data (dict): additional data to update

        """

        keys = ['id']
        entity.update(data)
        self.__target[table].upsert(entity, keys, ensure=False)

    def write_relation(self, table, keys, **data):
        """Write relation to target.

        Args:
            table (str): table name
            keys (str[]): filter keys
            data (dict): data to upsert

        """
        self.__target[table].upsert(data, keys, ensure=False)

    def commit(self):
        """Commit transaction on target.
        """
        self.__target.commit()

    def rollback(self):
        """Rollback transaction on target.
        """
        self.__target.rollback()
