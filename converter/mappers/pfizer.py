# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class PfizerMapper(base.Mapper):

    # Public

    table = 'data_pfizer'
    primary_key = 'nct_id'

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse[self.table]):

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
            logger.debug('Mapped: %s' % item[self.primary_key])
            time.sleep(0.1)

    def map_source(self):

        source_id = self.index('source',
            name='pfizer',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='pfizer',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=item['nct_id'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=None,
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='pfizer',
            primary_id=item['nct_id'],
            secondary_ids={'nct_id': item['nct_id'] },
            registration_date=item['study_start_date'],  # TODO: review
            public_title=item['title'],  # TODO: review
            brief_summary='',  # TODO: review
            scientific_title=None,  # TODO: review
            description=None,  # TODO: review

            # Recruitment
            recruitment_status=item['status'],
            eligibility_criteria={'criteria': item['overall_status']},
            target_sample_size=None,
            first_enrollment_date=item['study_start_date'],

            # Study design
            study_type=item['study_type'],
            study_design=None,  # TODO: review
            study_phase=None,  # TODO: review

            # Outcomes
            primary_outcomes=None,  # TODO: review
            secondary_outcomes=None,  # TODO: review

        )

        return trial_id

    def map_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={},  # TODO: serialization issue
        )

        self.write(db['trials_records'], ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):
        # TODO: check on scraper level
        pass

    def map_item_interventions(self, item, trial_id):
        # TODO: check on scraper level
        pass

    def map_item_locations(self, item, trial_id):
        # TODO: check on scraper level
        pass

    def map_item_organisations(self, item, trial_id):
        # TODO: check on scraper level
        pass

    def map_item_persons(self, item, trial_id):
        # TODO: check on scraper level
        pass


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = PrizerMapper(warehouse, database)
    mapper.map()
