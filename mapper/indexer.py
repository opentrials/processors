# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.dialects.postgres import ARRAY, UUID

logger = logging.getLogger(__name__)


class Indexer(object):

    # Public

    def __init__(self, warehouse):
        self.__warehouse = warehouse

    @property
    def warehouse(self):
        return self.__warehouse

    def index(self, target, **params):

        # Get method
        try:
            method = getattr(self, 'index_%s' % target)
        except AttributeError:
            message = 'Indexer %s doesn\'t support %s target.'
            message = message % (self, target)
            raise ValueError(message)

        # Index data
        id = method(**params)

        return id

    def index_source(self, name):

        # Create table
        if 'index_sources' not in self.warehouse:
            self.warehouse.create_table('index_sources',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = self.warehouse['index_sources'].find_one(name=name)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            self.warehouse['index_sources'].insert(item)
            logger.info('Indexed - source: %s' % name)

        # Return id
        return item['meta_id']

    def index_trial(self, nct_id=None, euctr_id=None,
            isrctn_id=None, scientific_title=None):

        # Create table
        if 'index_trials' not in self.warehouse:
            self.warehouse.create_table('index_trials',
                primary_id='meta_id', primary_type='String')

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
            self.warehouse['index_trials'].insert(item)
            logger.info('Indexed - trial: %s - %s - %s - <scientific_title>' %
                (nct_id, euctr_id, isrctn_id))

        # Return id
        return item['meta_id']

    def index_problem(self, name):

        # Create table
        if 'index_problems' not in self.warehouse:
            self.warehouse.create_table('index_problems',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = self.warehouse['index_problems'].find_one(name=name)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            self.warehouse['index_problems'].insert(item)
            logger.info('Indexed - problem: %s' % name)

        # Return id
        return item['meta_id']

    def index_intervention(self, name):

        # Create table
        if 'index_interventions' not in self.warehouse:
            self.warehouse.create_table('index_interventions',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = self.warehouse['index_interventions'].find_one(name=name)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            self.warehouse['index_interventions'].insert(item)
            logger.info('Indexed - intervention: %s ' % name)

        # Return id
        return item['meta_id']

    def index_location(self, name):

        # Create table
        if 'index_locations' not in self.warehouse:
            self.warehouse.create_table('index_locations',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = self.warehouse['index_locations'].find_one(name=name)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            self.warehouse['index_locations'].insert(item)
            logger.info('Indexed - location: %s ' % name)

        # Return id
        return item['meta_id']

    def index_organisation(self, name):

        # Create table
        if 'index_organisations' not in self.warehouse:
            self.warehouse.create_table('index_organisations',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = self.warehouse['index_organisations'].find_one(name=name)

        # Create item
        if item is None:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            self.warehouse['index_organisations'].insert(item)
            logger.info('Indexed - organisation: %s' % name)

        return item['meta_id']

    def index_person(self, name, phones):

        # Create table
        if 'index_persons' not in self.warehouse:
            self.warehouse.create_table('index_persons',
                primary_id='meta_id', primary_type='String')

        # Get item
        item = None
        query = 'SELECT * FROM index_persons WHERE name = :name'
        if not phones:
            items = list(self.warehouse.query(query, name=name))
        else:
            query += 'AND ANY(phones) = :phone'
            for phone in phones:
                items = list(self.warehouse.query(
                    query, name=name, phones=phones))
                if items:
                    break

        # Create item
        if not items:
            item = {}
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['name'] = name
            item['phones'] = phones
            self.warehouse['index_persons'].insert(
                item, types={'phones': ARRAY(sa.Text)})
            logger.info('Indexed - person: %s' % name)

        # Update item
        else:
            item = items[0]
            item['phones'] = list(set(item['phones'] + phones))
            self.warehouse['index_persons'].update(item, ['meta_id'])

        return item['meta_id']
