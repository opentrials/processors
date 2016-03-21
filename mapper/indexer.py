# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime
from sqlalchemy.dialects.postgres import ARRAY, UUID

from .. import base
logger = logging.getLogger(__name__)


class Indexer(object):

    # Public

    def __init__(self, warehouse):
        self.__warehouse = warehouse

    def index(self, target, **kwargs):

        # Get method
        try:
            method = getattr(self, 'index_%s' % target)
        except AttributeError:
            message = 'Indexer %s doesn\'t support %s target.'
            message = message % (self, target)
            raise ValueError(message)

        # Index data
        id = method(item)

        return id

    def index_source(self, name, type):

        # Get item
        item = self.warehouse['index_sources'].find_one(name=name, type=type)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['type'] = type
            self.warehouse['index_sources'].insert(
                item, ensure=True, types={'meta_id': UUID})
            logger.info('Indexed - source: %s' % item['meta_id'])

        # Return id
        return index['meta_id']

    def index_trial(self, nct_id=None, euctr_id=None,
            isrctn_id=None, scientific_title=None):

        # Get item
        item = None
        for key in ['nct_id', 'euctr_id', 'isrctn_id', 'scientific_title']:
            value = locals()[key]
            if not value:
                continue
            item = self.warehouse['index_trials'].find_one(**{key: value})
            if item is not None:
                break

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['nct_id'] = nct_id
            item['euctr_id'] = euctr_id
            item['isrctn_id'] = isrctn_id
            item['scientific_title'] = scientific_title
            self.warehouse['index_trials'].insert(
                item, ensure=True, types={'meta_id': UUID})
            logger.info('Indexed - trial: %s' % item['meta_id'])

        # Return id
        return item['meta_id']

    def index_problem(self, name, type):

        # Get item
        item = self.warehouse['index_problems'].find_one(name=name, type=type)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['type'] = type
            self.warehouse['index_source'].insert(
                item, ensure=True, types={'meta_id': UUID})
            logger.info('Indexed - source: %s' % item['meta_id'])

        # Return id
        return index['meta_id']

    def index_intervention(self, name, type):

        # Get item
        item = self.warehouse['index_interventions'].find_one(name=name, type=type)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['type'] = type
            self.warehouse['index_interventions'].insert(
                item, ensure=True, types={'meta_id': UUID})
            logger.info('Indexed - intervention: %s' % item['meta_id'])

        # Return id
        return index['meta_id']

    def index_location(self, name, type):

        # Get item
        item = self.warehouse['index_locations'].find_one(name=name, type=type)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['type'] = type
            self.warehouse['index_locations'].insert(
                item, ensure=True, types={'meta_id': UUID})
            logger.info('Indexed - location: %s' % item['meta_id'])

        # Return id
        return index['meta_id']

    def index_organisation(self, name, phones):

        # Get item
        item = None
        if 'index_organisations' in self.warehouse:
            query = 'SELECT * FROM index_organisations '
            query =+ 'WHERE name = :name AND ANY(phones) = :phone'
            for phone in phones:
                item = self.warehouse.query(query, name=name, phones=phones)
                if item is not None:
                    break

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['phones'] = phones
            self.warehouse['index_organisations'].insert(
                item, ensure=True, types={'meta_id': UUID, 'phones': ARRAY})
            logger.info('Indexed - organisation: %s' % item['meta_id'])

        # Update item
        else:
            item['phones'] = list(set(item['phones'] + phones))
            self.warehouse['index_organisations'].update(item, ['meta_id'], ensure=True)

        return item['meta_id']

    def index_person(self, name, phones):

        # Get item
        item = None
        if 'index_persons' in self.warehouse:
            query = 'SELECT * FROM index_persons '
            query =+ 'WHERE name = :name AND ANY(phones) = :phone'
            for phone in phones:
                item = self.warehouse.query(query, name=name, phones=phones)
                if item is not None:
                    break

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['phones'] = phones
            self.warehouse['index_persons'].insert(
                item, ensure=True, types={'meta_id': UUID, 'phones': ARRAY})
            logger.info('Indexed - person: %s' % item['meta_id'])

        # Update item
        else:
            item['phones'] = list(set(item['phones'] + phones))
            self.warehouse['index_persons'].update(item, ['meta_id'], ensure=True)

        return item['meta_id']
