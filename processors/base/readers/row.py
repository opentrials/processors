# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid


# Module API

def read_rows(conn, dataset, table, orderby, bufsize=100, **filter):
    """Read rows.

    Args:
        conn (dict): connection dict
        dataset (str): dataset name (e.g. warehouse/database)
        table (str): table name
        order_by (str): how to order rows
        bufsize (int): how many rows to get per query
        filter (dict): additional field filter

    Yields:
        dict: the next row from table

    """
    offset = 0
    query = filter
    query['order_by'] = orderby
    while True:
        query['_offset'] = offset
        query['_limit'] = bufsize
        count = conn[dataset][table].find(return_count=True, **query)
        if not count:
            break
        rows = conn[dataset][table].find(**query)
        offset += bufsize
        for row in rows:
            # Fixing hex representation
            for field in ['id', 'meta_id']:
                if field in row:
                    row[field] = uuid.UUID(row[field]).hex
            yield row
