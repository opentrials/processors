# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def index_trial(source,
        nct_id=None, euctr_id=None, isrctn_id=None, scientific_title=None):
    """Index trial (of not already exists) and return id.

    Args:
        source (object): source dataset object
        nct_id (str): nct identifier
        euctr_id (str): euctr identifier
        isrctn_id (str): isrctn identifier
        scientific_title (str): scientific title

    Returns:
        str: identifier

    """

    # Get index
    index = None
    for key in ['nct_id', 'euctr_id', 'isrctn_id', 'scientific_title']:
        index = source['index_sources'].find_one(**{key: locals()[key]})
        if index is not None:
            break

    # Create index
    if index is None:
        index = dict(name=name, type=type)
        index['meta_id'] = uuid.uuid4().hex
        index['meta_created'] = datetime.now()  # TODO: fix timezone
        index['meta_updated'] = datetime.now()  # TODO: fix timezone
        index['nct_id'] = nct_id
        index['euctr_id'] = euctr_id
        index['isrctn_id'] = isrctn_id
        index['scientific_title'] = scientific_title
        source['index_sources'].insert(index, ensure=True)
        logger.debug('Indexed - trial: %s' % item['meta_id'])

    # Return id
    return index['meta_id']
