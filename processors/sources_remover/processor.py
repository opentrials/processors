# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


def process(conf, conn):
    db = conn['database']
    source_ids = _parse_sources(conf.get('REMOVE_SOURCE_IDS'))

    if source_ids:
        try:
            logger.debug('Removing sources %s', source_ids)
            db.begin()
            db['sources'].delete(id=source_ids)
        except Exception:
            base.config.SENTRY.captureException()
            logger.debug('Rolling back')
            db.rollback()
        else:
            db.commit()
        finally:
            logger.debug('Done')
    else:
        logger.debug('No sources to remove')


def _parse_sources(source_ids_text):
    source_ids = (source_ids_text or '').split(',')
    return tuple([
        source_id.strip()
        for source_id in source_ids if source_id.strip()
    ])
