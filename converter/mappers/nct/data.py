# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset
import logging

from .. import helpers
from .sources import map_sources
from .trials import map_item_trials
logger = logging.getLogger(__name__)


def map_data():

    # Get connections
    source = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
    target = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])

    # Map sources
    source_id = map_sources(source, target)

    for item in helpers.table_read(source['nct']):

        # Map trials
        trial_id = map_item_trials(source, target, item)

        # Map records
        map_item_records(source, target, item, trial_id, source_id)

        # Map other entities
        map_item_problems(source, target, item, trial_id)
        map_item_interventions(source, target, item, trial_id)
        map_item_locations(source, target, item, trial_id)
        map_item_organisations(source, target, item, trial_id)
        map_item_personss(source, target, item, trial_id)

        # Log and sleep
        logger.debug('Mapped: %s' % item['nct_id'])
        time.sleep(0.1)
