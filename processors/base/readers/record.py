# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid


# Module API

def read_records(conn, table, bufsize=100, orderby='meta_id'):
    """Read records.

    Args:
        conn (dict): connection dict
        table (str): table name
        bufsize (int): how many items to get per query
        order_by (str): how to order items

    Yields:
        dict: the next item from table

    """
    offset = 0
    while True:
        query = {'_offset': offset, '_limit': bufsize, 'order_by': orderby}
        count = conn['warehouse'][table].find(return_count=True, **query)
        if not count:
            break
        items = conn['warehouse'][table].find(**query)
        offset += bufsize
        for item in items:
            item['meta_id'] = uuid.UUID(item['meta_id']).hex
            yield item
