# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class IctrpExtractor(base.Extractor):

    # Public

    table = 'data_ictrp'
    primary_key = 'main_id'

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
            name='ictrp',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='ictrp',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=None,
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['scientific_title'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='ictrp',
            primary_id=item['main_id'],
            secondary_ids={},
            registration_date=None,  # TODO: text on scrap layer
            public_title=item['pucli_title'],
            brief_summary='',  # TODO: review
            scientific_title=item['scientific_title'],  # TODO: review
            description=None,  # TODO: review

            # Recruitment
            recruitment_status=item['recruitment_status'],
            eligibility_criteria={'criteria': item['key_inclusion_exclusion_criteria']},
            target_sample_size=item['target_sample_size'],
            first_enrollment_date=None,  # TODO: text on scraper layer

            # Study design
            study_type=item['study_type'],
            study_design=item['study_design'],
            study_phase=item['study_phase'],

            # Outcomes
            primary_outcomes=item['primary_outcomes'],
            secondary_outcomes=item['secondary_outcomes'],

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

        for condition in item['health_conditions_or_problems_studied'] or []:

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

        # TODO: parse "drug: name"

        for intervention in item['interventions'] or []:

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

        for location in item['countries_of_recruitment'] or []:

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
        pass

    def map_item_persons(self, item, trial_id):
        pass
