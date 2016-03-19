# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import helpers
from . import base
logger = logging.getLogger(__name__)


class TrialConverter(object):

    # Public

    def convert(self, table):

        # Map sources
        source_id = convert_source()

        for item in self.read(table):

            # Map trials
            trial_id = self.convert_item_trial(item)

            # Map records
            self.convert_item_record(item, trial_id, source_id)

            # Map other entities
            self.convert_item_problems(item, trial_id)
            self.convert_item_interventions(item, trial_id)
            self.convert_item_locations(item, trial_id)
            self.convert_item_organisations(item, trial_id)
            self.convert_item_persons(item, trial_id)

            # Log and sleep
            logger.debug('Mapped: %s' % item['nct_id'])
            time.sleep(0.1)

    def convert_source(self):

        source_id = self.index('source',
            name='nct',
            type='register',
        )

        self.write('sources', ['id'],
            id=source_id,
            name='nct',
            type='register',
            data={},
        )

        return source_id

    def convert_item_trial(self, item):

        trial_id = self.index('trial',
            nct_id=item['nct_id'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_title'],
        )

        self.write('trials', ['id'],

            # General
            id=trial_id,
            primary_register='nct',
            primary_id=item['nct_id'],
            secondary_ids={'others': item['secondary_ids'] },
            registration_date=item['firstreceived_date'],
            public_title=item['brief_title'],
            brief_summary=item['brief_summary'] or '',  # TODO: review
            scientific_title=item['official_title'],
            description=item['detailed_description'],

            # Recruitment
            recruitment_status=item['overall_status'],
            eligibility_criteria=item['eligibility'],
            target_sample_size=item['enrollment_anticipated'],
            first_enrollment_date=item['start_date'],

            # Study design
            study_type=item['study_type'],
            study_design=item['study_design'],
            study_phase=item['phase'],

            # Outcomes
            primary_outcomes=item['primary_outcomes'] or [],
            secondary_outcomes=item['secondary_outcomes'] or [],

        )

        return trial_id

    def convert_item_record(self, item, trial_id, source_id):

        self.write('records', ['id'],
            id=item['meta_id'],
            source_id=source_id,
            type='trial',
            data={'nct_id': item['nct_id']},  # TODO: serialization issue
        )

        self.write(db['trials_records'], ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=item['meta_id'],
            role='primary',
            context={},
        )

    def convert_item_problems(self, item, trial_id):

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

    def convert_item_interventions(self, item, trial_id):

        for intervention in item['interventions'] or []:

            intervention_id = self.index('intervention',
                name=intervention['intervention_name'],
                type=None,
            )

            self.write('interventions', ['id'],
                id=intervention_id,
                name=intervention['intervention_name'],
                type=None,
                data={},
            )

            self.write('trials_interventions', ['trial_id', 'intervention_id'],
                trial_id=trial_id,
                intervention_id=intervention_id,
                role=None,
                context=intervention,
            )

    def convert_item_locations(self, item, trial_id):

        for location in item['location_countries'] or []:

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

    def convert_item_organisations(self, item, trial_id):

        for sponsor in item['sponsors'] or []:

            # TODO: get more information
            sponsor = sponsor.get('lead_sponsor', None)
            if sponsor is None:
                continue

            organisation_id = self.index('organisation',
                name=sponsor['agency'],
                type=None,
            )

            self.write('organisations', ['id'],
                id=organisation_id,
                name=sponsor['agency'],
                type=None,
                data={},
            )

            self.write('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=organisation_id,
                role='primary_sponsor',
                context={},
            )

    def convert_item_persons(self, item, trial_id):

        for person in item['overall_officials'] or []:

            # TODO: get more information
            if person.get('role', None) != 'Principal Investigator':
                continue

            person_id = self.index('person',
                name=person['last_name'],
                type=None,
            )

            self.write('persons', ['id'],
                id=person_id,
                name=person['last_name'],
                type=None,
                data={},
            )

            self.write('trials_persons', ['trial_id', 'person_id'],
                trial_id=trial_id,
                person_id=person_id,
                role='principal_investigator',
                context={},
            )
