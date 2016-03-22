# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


# Module API

class Finder(object):

    # Public

    def __init__(self, database):
        self.__database = database

    def find(self, table, links=None, facts=None, **filter):  # noqa

        # Create query
        # TODO: improve
        query = []
        where = []
        where_or = []
        query.append("SELECT * from %s" % table)
        if filter or facts:
            query.append("WHERE")
        if filter:
            for key, value in filter.items():
                where.append("%s = '%s'" % (key, value.replace("'", "''")))
        if links is not None:
            links = _clean_array(links)
            where_or.append("links && %s" % _make_array(links))
        if facts is not None:
            facts = _clean_array(facts)
            where_or.append("facts && %s" % _make_array(facts))
        where_or = " OR ".join(where_or)
        if where_or:
            where.append('(%s)' % where_or)
        query.append(" AND ".join(where))
        query = ' '.join(query)

        # Get entry
        entries = list(self.__database.query(query))
        timestamp = datetime.utcnow()
        existent = False

        # Create entry
        if not entries:
            entry = {}
            entry.update(filter)
            entry['id'] = uuid.uuid4().hex
            entry['created'] = timestamp
            entry['updated'] = timestamp
            entry['links'] = links or []
            entry['facts'] = facts or []
            entry.update(filter)

        # Update entry
        elif len(entries) == 1:
            existent = True
            entry = entries[0]
            entry['id'] = entry['id'].hex
            entry['updated'] = timestamp
            entry['links'] = list(set(entry['links'] + (links or [])))
            entry['facts'] = list(set(entry['facts'] + (facts or [])))
            entry.update(filter)

        # Too many entries
        else:
            message = 'Finding error: More than 1 entry: %s - %s - %s'
            message = message % (table, facts, filter)
            raise RuntimeError(message)

        return entry, existent


# Internal

# TODO: move to helpers
def _clean_array(iterable):
    array = []
    for element in iterable:
        if element and len(element) > 5:
            array.append(element)
    return array


# TODO: move to helpers
def _make_array(iterable):
    array = []
    for element in iterable:
        array.append("'%s'" % element.replace("'", "''"))
    return "ARRAY[%s]::text[]" % ', '.join(array)
