# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):
    """Remove duplicate records from EUCTR"""

    query = "SELECT eudract_number_with_country from euctr where eudract_number_with_country ~ '^EUCTR*';"

    count = 0
    for euctr_record in conn['warehouse'].query(query):
        eudract_id = euctr_record['eudract_number_with_country']
        try:
            conn['warehouse']['euctr'].delete(eudract_number_with_country=eudract_id)
        except Exception:
            logger.exception('Can\'t delete EUCTR record: %s', eudract_id)
        else:
            logger.info('Deleted EUCTR record: %s', eudract_id)
            count += 1
    logger.info('Removed %s EUCTR records', count)
