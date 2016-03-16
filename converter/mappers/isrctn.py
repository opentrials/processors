# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class IsrctnMapper(base.Mapper):

    # Public

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse['isrctn']):

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
            logger.debug('Mapped: %s' % item['nct_id'])
            time.sleep(0.1)

    def map_source(self):

        source_id = upsert(db['sources'], ['name', 'type'], {
            'name': 'isrctn',
            'type': 'register',
            'data': {},
        })

    def map_item_trial(self, item):

        # Create mapping
        mapping = OrderedDict()
        mapping['nct_id'] = item['clinicaltrialsgov_number']
        mapping['euctr_id'] = None
        mapping['isrctn_id'] = item['isrctn_id']
        mapping['scientific_title'] = item['scientific_title']

        helpers.update_trial(
            conn=wh,
            mapping=mapping,
            identifier='isrctn::%s' % item['meta_uuid'])

        # trials

        # TODO: review
        try:
            target_sample_size = int(item['target_number_of_participants'])

        except Exception:
            target_sample_size = None
        trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

            # General
            'primary_register': 'isrctn',
            'primary_id': item['isrctn_id'],
            'secondary_ids': {
                'doi_isrctn': item['doi_isrctn_id'],  # TODO: remove isrct part
                'euctr': item['eudract_number'],
                'nct': item['clinicaltrialsgov_number'],
            },
            'registration_date': item['date_applied'],  # TODO: review
            'public_title': item['title'],
            'brief_summary': item['plain_english_summary'],
            'scientific_title': item['scientific_title'],
            'description': None,  # TODO: review

            # Recruitment
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {
                'inclusion': item['participant_inclusion_criteria'],
                'exclusion': item['participant_exclusion_criteria'],
            },
            'target_sample_size': target_sample_size,
            'first_enrollment_date': item['overall_trial_start_date'],

            # Study design
            'study_type': item['primary_study_design'],
            'study_design': item['study_design'],
            'study_phase': item['phase'] or 'N/A',  # TODO: review

            # Outcomes
            'primary_outcomes': item['primary_outcome_measures'] or [],
            'secondary_outcomes': item['secondary_outcome_measures'] or [],

        })

    def map_item_record(self, item, trial_id, source_id):

        record_id = item['meta_uuid']

        upsert(db['records'], ['id'], {
            'id': record_id,
            'source_id': source_id,
            'type': 'trial',
            'data': {'isrctn_id': item['isrctn_id']},  # TODO: serialization issue
        }, auto_id=False)

        upsert(db['trials_records'], ['trial_id', 'record_id'], {
            'trial_id': trial_id,
            'record_id': record_id,
            'role': 'primary',
            'context': {},
        }, auto_id=False)

    def map_item_problems(self, item, trial_id):
        # TODO: item['condition'] - free text
        pass

    def map_item_interventions(self, item, trial_id):
        # TODO: item['interventions'] - free text
        # TODO: item['drug_names'] - free text
        pass

    def map_item_locations(self, item, trial_id):

        # TODO: move to scraper
        countries = (item['countries_of_recruitment'] or '').split(',') or []

        for country in countries:

            location_id = upsert(db['locations'], ['name', 'type'], {
                'name': country,
                'type': 'country',
                'data': {},
            })

            upsert(db['trials_locations'], ['trial_id', 'location_id'], {
                'trial_id': trial_id,
                'location_id': location_id,
                'role': 'recruitment_countries',
                'context': {},
            }, auto_id=False)

    def map_item_organisations(self, item, trial_id):

        for sponsor in item['sponsors'] or []:

            organisation_id = upsert(db['organisations'], ['name'], {
                'name': sponsor['organisation'],
                'type': None,
                'data': sponsor,
            })

            upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
                'trial_id': trial_id,
                'organisation_id': organisation_id,
                'role': 'sponsor',
                'context': {},
            }, auto_id=False)

        for funder in item['funders'] or []:

            organisation_id = upsert(db['organisations'], ['name'], {
                'name': funder['funder_name'],
                'type': None,
                'data': funder,
            })

            upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
                'trial_id': trial_id,
                'organisation_id': organisation_id,
                'role': 'funder',
                'context': {},
            }, auto_id=False)

    def map_item_persons(self, item, trial_id):

        for person in item['contacts'] or []:

            name = person.get('primary_contact', person.get('additional_contact'))
            if not name:
                continue

            person_id = upsert(db['persons'], ['name'], {
                'name': name,
                'type': None,
                'data': {},
            })

            upsert(db['trials_persons'], ['trial_id', 'person_id'], {
                'trial_id': trial_id,
                'person_id': person_id,
                'role': None,
                'context': person,
            }, auto_id=False)


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = IsrctnMapper(warehouse, database)
    mapper.map()
