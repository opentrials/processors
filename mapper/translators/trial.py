# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import time
import logging
import hashlib

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

        # Map sources
        source_id = self.translate_source(None)

        sucess = 0
        errors = 0
        for item in self.__pipeline.read(self.__extractor.table):

            self.__pipeline.begin()

            try:

                # Map trials
                trial_id, primary = self.translate_trial(item)

                # Map records
                self.translate_record(item, trial_id, source_id, primary=primary)

                if primary:

                    # Map other entities
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
                sucess += 1
                self.__pipeline.commit()
                logger.info('Translated - trial: %s [%s]' % (trial_id, sucess))

            # Sleep to avoid node overloading
            time.sleep(0.1)

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
            logger.info('Created - source: %s' % (source['name']))

        return entry['id']

    def translate_trial(self, item):

        trial = self.__extractor.extract('trial',
            item=item,
        )

        facts=[
            _slugify(trial.get('nct_id', None)),
            _slugify(trial.get('euctr_id', None)),
            _slugify(trial.get('isrctn_id', None)),
            _slugify(trial.get('scientific_title', None), hash=True),
        ]

        entity, existent = self.__finder.find('trials',
            facts=facts,
        )

        # TODO: improve
        primary = True
        if existent:
            if trial['primary_register'] != 'nct':
                primary = False

        if primary:
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

        if not existent:
            logger.info('Created - trial: %s' % (trial['primary_id']))

        return entity['id'], primary

    def translate_record(self, item, trial_id, source_id, primary):

        role = 'secondary'
        if primary:
            role = 'primary'

        record = self.__extractor.extract('record',
            item=item,
        )

        entity, existent = self.__finder.find('records',
            id=item['meta_id'],
        )

        self.__pipeline.write_entity('records', entity,
            source_id=source_id,
            type=record.get('type', None),
            data=record.get('data', {}),
        )

        self.__pipeline.write_relation('trials_records', ['trial_id', 'record_id'],
            trial_id=trial_id,
            record_id=entity['id'],
            role=role,
            context=record.get('context', {}),
        )

        if not existent:
            logger.info('Created - record: %s' % (entity['id']))

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

            if not existent:
                logger.info('Created - problem: %s' % (problem['name']))

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

            if not existent:
                logger.info('Created - intervention: %s' % (intervention['name']))

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

            if not existent:
                logger.info('Created - location: %s' % (location['name']))

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

            if not existent:
                logger.info('Created - organisation: %s' % (organisation['name']))

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
                facts.append(_slugify(phone))

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

            if not existent:
                logger.info('Created - person: %s' % (person['name']))


# Internal

# TODO: use slugify package
def _slugify(string, hash=False):
    slug = None
    if string:
        slug = re.sub(r'\W', '', string).lower() or None
    if slug and hash:
        slug = hashlib.md5(slug).hexdigest()
    return slug
