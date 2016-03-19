# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime

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

        # Get index
        index = self.warehouse['index_source'].find_one(name=name, type=type)

        # Create index
        if index is None:
            index = dict(name=name, type=type)
            index['meta_id'] = uuid.uuid4().hex
            index['meta_created'] = datetime.now()  # TODO: fix timezone
            index['meta_updated'] = datetime.now()  # TODO: fix timezone
            index['name'] = name
            index['type'] = type
            self.warehouse['index_source'].insert(index, ensure=True)
            logger.debug('Indexed - source: %s' % item['meta_id'])

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
            item = dict(name=name, type=type)
            item['meta_id'] = uuid.uuid4().hex
            item['meta_created'] = datetime.now()  # TODO: fix timezone
            item['meta_updated'] = datetime.now()  # TODO: fix timezone
            item['nct_id'] = nct_id
            item['euctr_id'] = euctr_id
            item['isrctn_id'] = isrctn_id
            item['scientific_title'] = scientific_title
            self.warehouse['index_trials'].insert(item, ensure=True)
            logger.debug('Indexed - trial: %s' % item['meta_id'])

        # Return id
        return item['meta_id']
