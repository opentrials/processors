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


class SourceIndexer(base.Indexer):

    # Public

    table = 'index_sources'

    def index(self, name, type):

        # Get index
        index = self.warehouse[self.table].find_one(name=name, type=type)

        # Create index
        if index is None:
            index = dict(name=name, type=type)
            index['meta_id'] = uuid.uuid4().hex
            index['meta_created'] = datetime.now()  # TODO: fix timezone
            index['meta_updated'] = datetime.now()  # TODO: fix timezone
            index['name'] = name
            index['type'] = type
            self.warehouse[self.table].insert(index, ensure=True)
            logger.debug('Indexed - source: %s' % item['meta_id'])

        # Return id
        return index['meta_id']
