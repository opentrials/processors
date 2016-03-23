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

        # Get entities
        entities = list(self.__database.query(query))
        timestamp = datetime.utcnow()
        existent = False

        # Create entity
        if not entities:
            entity = {}
            entity.update(filter)
            entity['id'] = uuid.uuid4().hex
            entity['created'] = timestamp
            entity['updated'] = timestamp
            entity['links'] = links or []
            entity['facts'] = facts or []
            entity.update(filter)

        # Update entity
        elif len(entities) == 1:
            existent = True
            entity = entities[0]
            entity['id'] = entity['id'].hex
            entity['updated'] = timestamp
            entity['links'] = list(set(entity['links'] + (links or [])))
            entity['facts'] = list(set(entity['facts'] + (facts or [])))
            entity.update(filter)

        # Too many entities
        else:
            message = 'Finding error: More than 1 entity: %s - %s - %s'
            message = message % (table, facts, filter)
            raise RuntimeError(message)

        return entity, existent


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
