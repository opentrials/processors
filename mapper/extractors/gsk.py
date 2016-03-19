# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class GskExtractor(base.Extractor):

    # Public

    table = 'gsk'
    primary_key = 'study_id'

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
            name='gsk',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='gsk',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=item['clinicaltrialsgov_identifier'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_study_title'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='gsk',
            primary_id=item['study_id'],
            secondary_ids={
                'nct': item['clinicaltrialsgov_identifier'],
                'others': item['secondary_ids'],
            },
            registration_date=item['first_received'],  # TODO: review
            public_title=item['study_title'],
            brief_summary=item['brief_summary'] or '',  # TODO: review
            scientific_title=item['official_study_title'],  # TODO: review
            description=item['detailed_description'],

            # Recruitment
            recruitment_status=item['study_recruitment_status'],
            eligibility_criteria={
                'criteria': item['eligibility_criteria'],  # TODO: bad text - fix on scraper
            },
            target_sample_size=item['enrollment'],  # TODO: review
            first_enrollment_date=item['study_start_date'],

            # Study design
            study_type=item['study_type'],  # TODO: review
            study_design=item['study_design'] or 'N/A',  # TODO: review
            study_phase=item['phase'] or 'N/A',  # TODO: review

            # Outcomes
            primary_outcomes=item['primary_outcomes'] or [],
            secondary_outcomes=item['secondary_outcomes'] or [],

        )

    def map_item_record(self, item, trial_id, source_id):

        record_id = item['meta_uuid']

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={'study_id': item['study_id']},  # TODO: serialization issue
        )

        self.write('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):

        for condition in item['conditions'] or []:

            problem_id = self.index('problem',
                name=condition,
                type=None,
            )

            self.write('problems', ['id'],
                id=problem_id,
                name=condition,
                type=None,
                data={},
            )

            self.write('trials_problems', ['trial_id', 'problem_id'],
                trial_id=trial_id,
                problem_id=problem_id,
                role=None,
                context={},
            )

    def map_item_interventions(self, item, trial_id):
        # TODO: item['interventions'] - reimplement on scraper - array -> dict
        pass

    def map_item_locations(self, item, trial_id):
        # TODO: no recruitment countries field
        pass

    def map_item_organisations(self, item, trial_id):
        # TODO: discover how to get it/fix it on scraper
        pass

    def map_item_persons(self, item, trial_id):
        # TODO: discover how to get it/fix it on scraper
        pass


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = GskMapper(warehouse, database)
    mapper.map()
