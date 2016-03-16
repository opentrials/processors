# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class TakedaMapper(base.Mapper):

    # Public

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse['takeda']):

            # Map trials
            trial_id = self.map_item_trial(item)

            # Map records
            self.map_item_record(item, trial_id, source_id)

            # Map other entities
            self.map_item_problems(item, trial_id)
            self.map_item_interventions(item, trial_id)
            self.map_item_locations(item, trial_id)
            self.map_item_organisations(item, trial_id)
            self.map_item_persons(item, trial_id)

            # Log and sleep
            logger.debug('Mapped: %s' % item['takeda_trial_id'])
            time.sleep(0.1)

    def map_source(self):
        pass

    def map_item_trial(self, item):
        pass

    def map_item_record(self, item, trial_id, source_id):
        pass

    def map_item_problems(self, item, trial_id):
        pass

    def map_item_interventions(self, item, trial_id):
        pass

    def map_item_locations(self, item, trial_id):
        pass

    def map_item_organisations(self, item, trial_id):
        pass

    def map_item_persons(self, item, trial_id):
        pass


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = TakedaMapper(warehouse, database)
    mapper.map()
