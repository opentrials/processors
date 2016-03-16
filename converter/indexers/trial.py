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


class TrialIndexer(base.Indexer):

    # Public

    table = 'index_trials'

    def index(self, nct_id=None, euctr_id=None,
            isrctn_id=None, scientific_title=None):

        # Get item
        item = None
        for key in ['nct_id', 'euctr_id', 'isrctn_id', 'scientific_title']:
            value = locals()[key]
            if not value:
                continue
            item = self.warehouse[self.table].find_one(**{key: value})
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
            self.warehouse[self.table].insert(item, ensure=True)
            logger.debug('Indexed - trial: %s' % item['meta_id'])

        # Return id
        return item['meta_id']
