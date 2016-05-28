# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid


# Module API

def read_objects(conn, table, first=False, slug=None, facts=None, **filter):
    """Read objects.

    Args:
        conn (dict): connection dict
        table (str): table name
        first (bool): return first object if True
        slug (str): string to check (should be slugified)
        facts (list): strings to check (should be slugified)
        filter (dict): additional field filter

    Returns:
        dict[]/dict/None: list of objects/object/None if not object

    """

    # Get objects
    query = _make_query(table, slug, facts, **filter)
    objects = list(conn['database'].query(query))

    # Fix id type
    for object in objects:
        if isinstance(object['id'], uuid.UUID):
            object['id'] = object['id'].hex

    # If first object requested
    if first:
        if not objects:
            return None
        return objects[0]

    return objects


# Internal

def _make_query(table, slug, facts, **filter):
    """Make filtering query.
    """
    query = []
    where = []
    query.append("SELECT * from %s" % table)
    if filter:
        for key, value in filter.items():
            where.append("%s = '%s'" % (key, value.replace("'", "''")))
    if slug is not None:
        where.append("slug = '%s'" % slug)
    if facts is not None:
        where.append("facts && %s" % _make_array(facts))
    if where:
        query.append("WHERE")
    query.append(" AND ".join(where))
    query = ' '.join(query)
    return query


def _make_array(array):
    """Create PostgreSQL array string from python array.
    """
    result = []
    for element in array:
        result.append("'%s'" % element.replace("'", "''"))
    return "ARRAY[%s]::text[]" % ', '.join(result)
