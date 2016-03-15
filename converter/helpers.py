# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid


def table_upsert(table, data, keys=['id']):
    """Upsert data to table

    Args:
        table (object): datastore table object
        data (dict): data to upsert to the table
        key (str[]): key to decide update or insert

    """
    table.upsert(data, keys, ensure=False)


def table_read(table, bufsize=10, orderby='meta_id'):
    """Yield items from table.

    Args:
        table (object): datastore table object
        bufsize (int): how many items to query per request
        orderby (str): field to order by

    Yields:
        dict: the next item from table

    """
    offset = 0
    while True:
        query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
        count = table.find(return_count=True, **query)
        if not count:
            break
        items = table.find(**query)
        offset += bufsize
        for item in items:
            yield item
