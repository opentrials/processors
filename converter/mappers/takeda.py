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

    table = 'data_takeda'
    primary_key = 'takeda_trial_id'

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
            name='takeda',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='takeda',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=item['nct_number'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_title'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='takeda',
            primary_id=item['takeda_trial_id'],
            secondary_ids={'nct': item['nct_number'] },
            registration_date=item['start_date'], # TODO: review
            public_title=item['official_title'], # TODO: review
            brief_summary=item['brief_summary'] or '',  # TODO: review
            scientific_title=item['official_title'],
            description=item['detailed_description'],

            # Recruitment
            recruitment_status=item['recruitment_status'],
            eligibility_criteria={'criteria': item['eligibility_criteria']},
            target_sample_size=None,
            first_enrollment_date=item['start_date'],

            # Study design
            study_type=item['trial_type'],
            study_design=item['trial_design'],
            study_phase=item['trial_phase'],

            # Outcomes
            primary_outcomes=None,  # TODO: review free test
            secondary_outcomes=None,  # TODO: review free test

        )

    def map_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={},  # TODO: serialization issue
        )

        self.write(db['trials_records'], ['trial_id', 'record_id'],
            trial_id=item['meta_id'],
            record_id=item['meta_uuid'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):

        problem_id = self.index('problem',
            name=item['condition'],
            type=None,
        )

        self.write('problems', ['id'],
            id=problem_id,
            name=item['condition'],
            type='condition',
            data={},
        )

        self.write('trials_problems', ['trial_id', 'problem_id'],
            trial_id=trial_id,
            problem_id=problem_id,
            role=None,
            context={},
        )

    def map_item_interventions(self, item, trial_id):

        for intervention in item['compound'] or []:

            intervention_id = self.index('intervention',
                name=intervention,
                type=None,
            )

            self.write('interventions', ['id'],
                id=intervention_id,
                name=intervention,
                type=None,
                data={},
            )

            self.write('trials_interventions', ['trial_id', 'intervention_id'],
                trial_id=trial_id,
                intervention_id=intervention_id,
                role=None,
                context={},
            )

    def map_item_locations(self, item, trial_id):

        for location in item['locations'] or []:

            location_id = self.index('location',
                name=location,
                type='country',
            )

            self.write('locations', ['id'],
                id=location_id,
                name=location,
                type='country',
                data={},
            )

            self.write('trials_locations', ['trial_id', 'location_id'],
                trial_id=trial_id,
                location_id=location_id,
                role='recruitment_countries',
                context={},
            )

    def map_item_organisations(self, item, trial_id):
        # TODO: review on scraper level
        pass

    def map_item_persons(self, item, trial_id):
        # TODO: review on scraper level
        pass


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = TakedaMapper(warehouse, database)
    mapper.map()
