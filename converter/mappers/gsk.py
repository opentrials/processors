# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class GskMapper(base.Mapper):

    # Public

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse['gsk']):

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
            'name': 'gsk',
            'type': 'register',
            'data': {},
        })

    def map_item_trial(self, item):

        trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

            # General
            'primary_register': 'gsk',
            'primary_id': item['study_id'],
            'secondary_ids': {
                'nct': item['clinicaltrialsgov_identifier'],
                'others': item['secondary_ids'],
            },
            'registration_date': item['first_received'],  # TODO: review
            'public_title': item['study_title'],
            'brief_summary': item['brief_summary'] or '',  # TODO: review
            'scientific_title': item['official_study_title'],  # TODO: review
            'description': item['detailed_description'],

            # Recruitment
            'recruitment_status': item['study_recruitment_status'],
            'eligibility_criteria': {
                'criteria': item['eligibility_criteria'],  # TODO: bad text - fix on scraper
            },
            'target_sample_size': item['enrollment'],  # TODO: review
            'first_enrollment_date': item['study_start_date'],

            # Study design
            'study_type': item['study_type'],  # TODO: review
            'study_design': item['study_design'] or 'N/A',  # TODO: review
            'study_phase': item['phase'] or 'N/A',  # TODO: review

            # Outcomes
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['secondary_outcomes'] or [],

        })

    def map_item_record(self, item, trial_id, source_id):

        record_id = item['meta_uuid']

        upsert(db['records'], ['id'], {
            'id': record_id,
            'source_id': source_id,
            'type': 'trial',
            'data': {'study_id': item['study_id']},  # TODO: serialization issue
        }, auto_id=False)

        upsert(db['trials_records'], ['trial_id', 'record_id'], {
            'trial_id': trial_id,
            'record_id': record_id,
            'role': 'primary',
            'context': {},
        }, auto_id=False)

    def map_item_problems(self, item, trial_id):

        for condition in item['conditions'] or []:

            problem_id = upsert(db['problems'], ['name', 'type'], {
                'name': condition,
                'type': None,
                'data': {},
            })

            upsert(db['trials_problems'], ['trial_id', 'problem_id'], {
                'trial_id': trial_id,
                'problem_id': problem_id,
                'role': None,
                'context': {},
            }, auto_id=False)

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
