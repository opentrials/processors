# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import logging

from . import base
logger = logging.getLogger(__name__)


class TrialTranslator(base.Translator):

    # Public

    basis = 'warehouse'

    def translate(self):

        # Map sources
        source_id = self.translate_source(None)

        count = 0
        for item in self.read():

            try:

                # Map trials
                trial_id, primary_id = self.translate_trial(item)

                # Map records
                self.translate_record(item, trial_id, source_id)

                # Map other entities
                self.translate_problems(item, trial_id)
                self.translate_interventions(item, trial_id)
                self.translate_locations(item, trial_id)
                self.translate_organisations(item, trial_id)
                self.translate_persons(item, trial_id)

                # Log and sleep
                count += 1
                logger.info('Translated - trial: %s [%s]' %
                    (primary_id, count))
                time.sleep(0.1)

            except Exception as exception:

                # Log error
                logger.warning('Translation error: %s' % repr(exception))

    def translate_source(self, item):

        source = self.extract('source',
            item=item,
        )

        source_id = self.index('source',
            name=source['name'],
        )

        self.write('sources', ['id'],
            id=source_id,
            name=source['name'],
            type=source.get('type', None),
            data=source.get('data', {}),
        )

        return source_id

    def translate_trial(self, item):

        trial = self.extract('trial',
            item=item,
        )

        trial_id = self.index('trial',
            nct_id=trial.get('nct_id', None),
            euctr_id=trial.get('euctr_id', None),
            isrctn_id=trial.get('isrctn_id', None),
            scientific_title=trial.get('scientific_title', None),
        )

        self.write('trials', ['id'],
            id=trial_id,
            primary_register=trial['primary_register'],
            primary_id=trial['primary_id'],
            secondary_ids=trial['secondary_ids'],
            registration_date=trial['registration_date'],
            public_title=trial['public_title'],
            brief_summary=trial['brief_summary'],
            scientific_title=trial.get('scientific_title', None),
            description=trial.get('descriptions', None),
            recruitment_status=trial['recruitment_status'],
            eligibility_criteria=trial['eligibility_criteria'],
            target_sample_size=trial.get('target_sample_size', None),
            first_enrollment_date=trial.get('first_enrollment_date', None),
            study_type=trial['study_type'],
            study_design=trial['study_design'],
            study_phase=trial['study_phase'],
            primary_outcomes=trial.get('primary_outcomes', None),
            secondary_outcomes=trial.get('primary_outcomes', None),
        )

        return (trial_id, trial['primary_id'])

    def translate_record(self, item, trial_id, source_id):

        record = self.extract('record',
            item=item,
        )

        record_id = item['meta_id']

        self.write('records', ['id'],
            id=record_id,
            source_id=source_id,
            type=record.get('type', None),
            data=record.get('data', {}),
        )

        self.write('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=record_id,
            role=record.get('role', None),
            context=record.get('context', {}),
        )

    def translate_problems(self, item, trial_id):

        problems = self.extract('problems',
            item=item,
        )

        for problem in problems:

            problem_id = self.index('problem',
                name=problem['name'],
            )

            self.write('problems', ['id'],
                id=problem_id,
                name=problem['name'],
                type=problem.get('type', None),
                data=problem.get('data', {}),
            )

            self.write('trials_problems', ['trial_id', 'problem_id'],
                trial_id=trial_id,
                problem_id=problem_id,
                role=problem.get('role', None),
                context=problem.get('context', {}),
            )

    def translate_interventions(self, item, trial_id):

        interventions = self.extract('interventions',
            item=item,
        )

        for intervention in interventions:

            intervention_id = self.index('intervention',
                name=intervention['name'],
            )

            self.write('interventions', ['id'],
                id=intervention_id,
                name=intervention['name'],
                type=intervention.get('type', None),
                data=intervention.get('data', {}),
            )

            self.write('trials_interventions', ['trial_id', 'intervention_id'],
                trial_id=trial_id,
                intervention_id=intervention_id,
                role=intervention.get('role', None),
                context=intervention.get('context', {}),
            )

    def translate_locations(self, item, trial_id):

        locations = self.extract('locations',
            item=item,
        )

        for location in locations:

            location_id = self.index('location',
                name=location['name'],
            )

            self.write('locations', ['id'],
                id=location_id,
                name=location['name'],
                type=location.get('type', None),
                data=location.get('data', {}),
            )

            self.write('trials_locations', ['trial_id', 'location_id'],
                trial_id=trial_id,
                location_id=location_id,
                role=location.get('role', None),
                context=location.get('context', {}),
            )

    def translate_organisations(self, item, trial_id):

        organisations = self.extract('organisations',
            item=item,
        )

        for organisation in organisations:

            organisation_id = self.index('organisation',
                name=organisation['name'],
            )

            self.write('organisations', ['id'],
                id=organisation_id,
                name=organisation['name'],
                type=organisation.get('type', None),
                data=organisation.get('data', {}),
            )

            self.write('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=organisation_id,
                role=organisation.get('role', None),
                context=organisation.get('context', {}),
            )

    def translate_persons(self, item, trial_id):

        persons = self.extract('persons',
            item=item,
        )

        for person in persons:

            person_id = self.index('person',
                name=person['name'],
                phones=person.get('phones', []),
            )

            self.write('persons', ['id'],
                id=person_id,
                name=person['name'],
                type=person.get('type', None),
                data=person.get('data', {}),
            )

            self.write('trials_persons', ['trial_id', 'person_id'],
                trial_id=trial_id,
                person_id=person_id,
                role=person.get('role', None),
                context=person.get('context', {}),
            )
