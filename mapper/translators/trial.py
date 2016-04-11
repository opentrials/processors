# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
# import time
import logging

from .. import helpers
from .. import extractors
from ..finder import Finder
from ..pipeline import Pipeline
from . import base
logger = logging.getLogger(__name__)


# Module API

class TrialTranslator(base.Translator):
    """Trial based translator from warehouse to database.
    """

    # Public

    def __init__(self, warehouse, database, extractor):

        self.__extractor = getattr(extractors, extractor.capitalize())()
        self.__pipeline = Pipeline(source=warehouse, target=database)
        self.__finder = Finder(database)

        if self.__extractor.store != 'warehouse':
            message = 'Translator and extractor are not compatible: %s-%s'
            message = message % (self, self.__extractor)
            raise ValueError(message)

    def translate(self):

        # Translate source
        source_id = self.translate_source(None)

        success = 0
        errors = 0
        for item in self.__pipeline.read(self.__extractor.table):

            self.__pipeline.begin()

            try:

                # Translate trial
                trial_id, trial_data, primary = self.translate_trial(item)

                # Translate trialrecord
                self.translate_trialrecord(item,
                    trial_id=trial_id,
                    trial_data=trial_data,
                    source_id=source_id,
                    primary=primary)

                if primary:

                    # Translate other entities
                    self.translate_problems(item, trial_id)
                    self.translate_interventions(item, trial_id)
                    self.translate_locations(item, trial_id)
                    self.translate_organisations(item, trial_id)
                    self.translate_persons(item, trial_id)

            except Exception as exception:
                errors += 1
                self.__pipeline.rollback()
                logger.warning('Translation error: %s [%s]' % (repr(exception), errors))

            else:
                success += 1
                self.__pipeline.commit()
                logger.debug('Translated - trial: %s [%s]' % (trial_id, success))

            if not success % 100:
                logger.info('Transated %s trials [%s]' % (success, self.__extractor.table))

            # Sleep to avoid node overloading
            # time.sleep(0.1)

    def translate_source(self, item):

        source = self.__extractor.extract('source',
            item=item,
        )

        entry, existent = self.__finder.find('sources',
            name=source['name'],
        )

        self.__pipeline.write_entity('sources', entry,
            type=source.get('type', None),
            data=source.get('data', {}),
        )

        if not existent:
            logger.debug('Created - source: %s' % (source['name']))

        return entry['id']

    def translate_trial(self, item):

        trial = self.__extractor.extract('trial',
            item=item,
        )

        facts=[
            helpers.slugify(trial.get('nct_id', None)),
            helpers.slugify(trial.get('euctr_id', None)),
            helpers.slugify(trial.get('isrctn_id', None)),
            helpers.slugify(trial.get('scientific_title', None), hash=True),
        ]

        entity, existent = self.__finder.find('trials',
            facts=facts,
        )

        # TODO: review
        # Decide item role based on entity we've found:
        # - primary - create/update all entities and relations
        # - secondary - only add secondary trialrecord
        if not existent:
            # New trial - primary (create)
            primary = True
        if existent:
            # Existent trial
            if entity['primary_id'] == trial['primary_id']:
                # The same item - primary (update)
                primary = True
            else:
                # Different item
                if entity['primary_register'] == self.__extractor.table:
                    # Item from the same register - secondary
                    primary = False
                elif entity['primary_register'] in self.__extractor.heads:
                    # Item from low priority register - secondary
                    primary = False
                else:
                    # Item from high priority register - primary
                    primary = True

        if primary:
            # Update trial
            self.__pipeline.write_entity('trials', entity,
                primary_register=trial['primary_register'],
                primary_id=trial['primary_id'],
                secondary_ids=trial['secondary_ids'],
                registration_date=trial['registration_date'],
                public_title=trial['public_title'],
                brief_summary=trial['brief_summary'],
                scientific_title=trial.get('scientific_title', None),
                description=trial.get('description', None),
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
        else:
            # Just update links, facts (etc)
            self.__pipeline.write_entity('trials', entity)

        if existent:
            logger.debug('Matched - trial: %s (primary:%s)' % (trial['primary_id'], primary))
        else:
            logger.debug('Created - trial: %s (primary: True)' % (trial['primary_id']))

        return entity['id'], trial, primary

    def translate_trialrecord(self, item, trial_id, trial_data, source_id, primary):

        role = 'secondary'
        if primary:
            role = 'primary'

        entity, existent = self.__finder.find('trialrecords',
            id=item['meta_id'],
        )

        self.__pipeline.write_entity('trialrecords', entity,
            source_id=source_id,
            source_url=item['meta_source'],
            source_data=json.dumps(item, cls=helpers.JSONEncoder),
            created_at=item['meta_created'],
            updated_at=item['meta_updated'],
            primary_register=trial_data['primary_register'],
            primary_id=trial_data['primary_id'],
            secondary_ids=trial_data['secondary_ids'],
            registration_date=trial_data['registration_date'],
            public_title=trial_data['public_title'],
            brief_summary=trial_data['brief_summary'],
            scientific_title=trial_data.get('scientific_title', None),
            description=trial_data.get('description', None),
            recruitment_status=trial_data['recruitment_status'],
            eligibility_criteria=trial_data['eligibility_criteria'],
            target_sample_size=trial_data.get('target_sample_size', None),
            first_enrollment_date=trial_data.get('first_enrollment_date', None),
            study_type=trial_data['study_type'],
            study_design=trial_data['study_design'],
            study_phase=trial_data['study_phase'],
            primary_outcomes=trial_data.get('primary_outcomes', None),
            secondary_outcomes=trial_data.get('primary_outcomes', None),
        )

        # Make all existent trialrecords secondary
        if primary:
            self.__pipeline.update('trials_trialrecords', ['trial_id'],
                trial_id=trial_id,
                role='secondary',
            )

        self.__pipeline.write_relation('trials_trialrecords', ['trial_id', 'trialrecord_id'],
            trial_id=trial_id,
            trialrecord_id=entity['id'],
            role=role,
            context={},
        )

        if existent:
            logger.debug('Matched - trialrecord: %s' % (entity['id']))
        else:
            logger.debug('Created - trialrecord: %s' % (entity['id']))

    def translate_problems(self, item, trial_id):

        problems = self.__extractor.extract('problems',
            item=item,
        )

        self.__pipeline.delete('trials_problems',
            trial_id=trial_id,
        )

        for problem in problems:

            entity, existent = self.__finder.find('problems',
                name=problem['name'],
            )

            self.__pipeline.write_entity('problems', entity,
                type=problem.get('type', None),
                data=problem.get('data', {}),
            )

            self.__pipeline.write_relation('trials_problems', ['trial_id', 'problem_id'],
                trial_id=trial_id,
                problem_id=entity['id'],
                role=problem.get('role', None),
                context=problem.get('context', {}),
            )

            if existent:
                logger.debug('Matched - problem: %s' % (problem['name']))
            else:
                logger.debug('Created - problem: %s' % (problem['name']))

    def translate_interventions(self, item, trial_id):

        interventions = self.__extractor.extract('interventions',
            item=item,
        )

        self.__pipeline.delete('trials_interventions',
            trial_id=trial_id,
        )

        for intervention in interventions:

            entity, existent = self.__finder.find('interventions',
                name=intervention['name'],
            )

            self.__pipeline.write_entity('interventions', entity,
                type=intervention.get('type', None),
                data=intervention.get('data', {}),
            )

            self.__pipeline.write_relation('trials_interventions', ['trial_id', 'intervention_id'],
                trial_id=trial_id,
                intervention_id=entity['id'],
                role=intervention.get('role', None),
                context=intervention.get('context', {}),
            )

            if existent:
                logger.debug('Matched - intervention: %s' % (intervention['name']))
            else:
                logger.debug('Created - intervention: %s' % (intervention['name']))

    def translate_locations(self, item, trial_id):

        locations = self.__extractor.extract('locations',
            item=item,
        )

        self.__pipeline.delete('trials_locations',
            trial_id=trial_id,
        )

        for location in locations:

            entity, existent = self.__finder.find('locations',
                name=location['name'],
            )

            self.__pipeline.write_entity('locations', entity,
                type=location.get('type', None),
                data=location.get('data', {}),
            )

            self.__pipeline.write_relation('trials_locations', ['trial_id', 'location_id'],
                trial_id=trial_id,
                location_id=entity['id'],
                role=location.get('role', None),
                context=location.get('context', {}),
            )

            if existent:
                logger.debug('Matched - location: %s' % (location['name']))
            else:
                logger.debug('Created - location: %s' % (location['name']))

    def translate_organisations(self, item, trial_id):

        organisations = self.__extractor.extract('organisations',
            item=item,
        )

        self.__pipeline.delete('trials_organisations',
            trial_id=trial_id,
        )

        for organisation in organisations:

            entity, existent = self.__finder.find('organisations',
                name=organisation['name'],
            )

            self.__pipeline.write_entity('organisations', entity,
                type=organisation.get('type', None),
                data=organisation.get('data', {}),
            )

            self.__pipeline.write_relation('trials_organisations', ['trial_id', 'organisation_id'],
                trial_id=trial_id,
                organisation_id=entity['id'],
                role=organisation.get('role', None),
                context=organisation.get('context', {}),
            )

            if existent:
                logger.debug('Matched - organisation: %s' % (organisation['name']))
            else:
                logger.debug('Created - organisation: %s' % (organisation['name']))

    def translate_persons(self, item, trial_id):

        persons = self.__extractor.extract('persons',
            item=item,
        )

        self.__pipeline.delete('trials_persons',
            trial_id=trial_id,
        )

        for person in persons:

            facts = []
            for phone in person.get('phones', []):
                facts.append(helpers.slugify(phone))

            entity, existent = self.__finder.find('persons',
                name=person['name'],
                links=[trial_id],
                facts=facts,
            )

            self.__pipeline.write_entity('persons', entity,
                type=person.get('type', None),
                data=person.get('data', {}),
            )

            self.__pipeline.write_relation('trials_persons', ['trial_id', 'person_id'],
                trial_id=trial_id,
                person_id=entity['id'],
                role=person.get('role', None),
                context=person.get('context', {}),
            )

            if existent:
                logger.debug('Matched - person: %s' % (person['name']))
            else:
                logger.debug('Created - person: %s' % (person['name']))
