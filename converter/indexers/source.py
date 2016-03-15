# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def index_source(tables, name, type):
    """Index source (of not already exists) and return id.

    Args:
        tables (object{}): dict of dataset table objects
        name (str): name of source
        type (str): type of source

    Returns:
        str: identifier

    """

    # Get index
    index = tables['index_sources'].find_one(name=name, type=type)

    # Create index
    if index is None:
        index = dict(name=name, type=type)
        index['meta_id'] = uuid.uuid4().hex
        index['meta_created'] = datetime.now()  # TODO: fix timezone
        index['meta_updated'] = datetime.now()  # TODO: fix timezone
        index['name'] = name
        index['type'] = type
        tables['index_sources'].insert(index, ensure=True)
        logger.debug('Indexed - source: %s' % item['meta_id'])

    # Return id
    return index['meta_id']
