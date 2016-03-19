# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class ActrnMapper(base.Extractor):

    # Public

    table = 'actrn'
    primary_key = 'trial_id'

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
            name='actrn',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='actrn',
            type='register',
            data={},
        )

        return source_id

    def map_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=item['nct_id'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_title'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='actrn',
            primary_id=item['trial_id'],
            secondary_ids={
                'others': item['secondary_ids'],
            },
            registration_date=item['date_registered'],
            public_title=item['public_title'],
            brief_summary=item['brief_summary'],
            scientific_title=item['scientific_title'],
            description=None,  # TODO: review

            # Recruitment
            recruitment_status=item['recruitment_status'],
            eligibility_criteria={
                'inclusion': item['key_inclusion_criteria'],
                'exclusion': item['key_exclusion_criteria'],
            },
            target_sample_size=item['target_sample_size'],
            first_enrollment_date=item['anticipated_date_of_first_participant_enrolment'],  # TODO: review

            # Study design
            study_type=item['study_type'],
            study_design='N/A',  # TODO: review
            study_phase=item['phase'] or 'N/A',  # TODO: review

            # Outcomes
            primary_outcomes=item['primary_outcomes'] or [],
            secondary_outcomes=item['secondary_outcomes'] or [],

        )

    def map_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={'actrn_id': item['trial_id']},  # TODO: serialization issue
        )

        upsert('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def map_item_problems(self, item, trial_id):
        # TODO: item['health_conditions_or_problems_studied'] - free text some time
        pass

    def map_item_interventions(self, item, trial_id):
        # TODO: item['intervention_codes'] - discover
        pass

    def map_item_locations(self, item, trial_id):
        # TODO: no recruitment countries
        pass

    def map_item_organisations(self, item, trial_id):

        for sponsor in item['sponsors'] or []:

            # TODO: process item['primary_sponsor']
            if 'name' not in sponsor:
                continue

            organisation_id = self.index('organisation',
                name=sponsor['name'],
                type=None,
            )

            self.write('organisations', ['id'],
                id=organisation_id,
                name=sponsor['name'],
                type=None,
                data=sponsor,
            )

            self.write('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=organisation_id,
                role='sponsor',  # TODO: review
                context={},
            )

    def map_item_persons(self, item, trial_id):

        # TODO: process item['principal_investigator']

        persons = []

        for role in ['public_queries', 'scientific_queries']:

            persons.append({
                'name': item[role]['name'],
                'role': role,
                'context': item[role],
            })

        for person in persons:

            person_id = self.index('person',
                name=person['name'],
                type=None,
            )

            self.write('persons', ['id'],
                id=person_id,
                name=person['name'],
                type=None,
                data={},
            )

            self.write('trials_persons', ['trial_id', 'person_id'],
                trial_id=trial_id,
                person_id=person_id,
                role=person['role'],
                context=person['context'],
            )
