# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .row import read_rows


# Module API

def read_records(conn, table, orderby='meta_id', bufsize=100, **filter):
    """Read rows.

    Args:
        conn (dict): connection dict
        table (str): table name
        order_by (str): how to order records
        bufsize (int): how many records to get per query
        filter (dict): additional field filter

    Yields:
        dict: the next record from table

    """
    for record in read_rows(conn, 'warehouse', table,
            orderby=orderby, bufsize=bufsize, **filter):
        yield record
