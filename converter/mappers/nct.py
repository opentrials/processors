# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .. import base
logger = logging.getLogger(__name__)


class NctMapper(base.Mapper):

    # Public

    def map(self):

        # Map sources
        source_id = map_source()

        for item in helpers.table_read(self.warehouse['nct']):

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

        id = indexers.index_source(self.warehouse,
            name='nct',
            type='register',
        )

        helpers.upsert(self.database['sources'], {
            'id': id,
            'name': 'nct',
            'type': 'register',
            'data': {},
        })

        return id

    def map_item_trial(self, item):

        id = indexers.index_trial(self.warehouse,
            nct_id=item['nct_id'],
            euctr_id=None,
            isrctn_id=None,
            scientific_title=item['official_title'],
        )

        helpers.upsert(self.database['trials'], {
            'id': id,
            'primary_register': 'nct',
            'primary_id': item['nct_id'],
            'secondary_ids': {'others': item['secondary_ids'] },
            'registration_date': item['firstreceived_date'],
            'public_title': item['brief_title'],
            'brief_summary': item['brief_summary'] or '',  # TODO: review
            'scientific_title': item['official_title'],
            'description': item['detailed_description'],
            'recruitment_status': item['overall_status'],
            'eligibility_criteria': item['eligibility'],
            'target_sample_size': item['enrollment_anticipated'],
            'first_enrollment_date': item['start_date'],
            'study_type': item['study_type'],
            'study_design': item['study_design'],
            'study_phase': item['phase'],
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['secondary_outcomes'] or [],
        })

        return id

    def map_item_record(self, item, trial_id, source_id):

        record_id = item['meta_uuid']

        helpers.upsert(db['records'], ['id'], {
            'id': record_id,
            'source_id': source_id,
            'type': 'trial',
            'data': {'nct_id': item['nct_id']},  # TODO: serialization issue
        }, auto_id=False)

        helpers.upsert(db['trials_records'], ['trial_id', 'record_id'], {
            'trial_id': trial_id,
            'record_id': record_id,
            'role': 'primary',
            'context': {},
        }, auto_id=False)

    def map_item_problems(self, item, trial_id):

        for condition in item['conditions'] or []:

            problem_id = helpers.upsert(db['problems'], ['name', 'type'], {
                'name': condition,
                'type': None,
                'data': {},
            })

            helpers.upsert(db['trials_problems'], ['trial_id', 'problem_id'], {
                'trial_id': trial_id,
                'problem_id': problem_id,
                'role': None,
                'context': {},
            }, auto_id=False)

    def map_item_interventions(self, item, trial_id):

        for intervention in item['interventions'] or []:

            intervention_id = helpers.upsert(db['interventions'], ['name', 'type'], {
                'name': intervention['intervention_name'],
                'type': None,
                'data': {},
            })

            helpers.upsert(db['trials_interventions'], ['trial_id', 'intervention_id'], {
                'trial_id': trial_id,
                'intervention_id': intervention_id,
                'role': None,
                'context': intervention,
            }, auto_id=False)

    def map_item_locations(self, item, trial_id):

        for location in item['location_countries'] or []:

            location_id = helpers.upsert(db['locations'], ['name', 'type'], {
                'name': location,
                'type': 'country',
                'data': {},
            })

            helpers.upsert(db['trials_locations'], ['trial_id', 'location_id'], {
                'trial_id': trial_id,
                'location_id': location_id,
                'role': 'recruitment_countries',
                'context': {},
            }, auto_id=False)

    def map_item_organisations(self, item, trial_id):

        for sponsor in item['sponsors'] or []:

            # TODO: get more information
            sponsor = sponsor.get('lead_sponsor', None)
            if sponsor is None:
                continue

            organisation_id = helpers.upsert(db['organisations'], ['name'], {
                'name': sponsor['agency'],
                'type': None,
                'data': {},
            })

            helpers.upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
                'trial_id': trial_id,
                'organisation_id': organisation_id,
                'role': 'primary_sponsor',
                'context': {},
            }, auto_id=False)

    def map_item_persons(self, item, trial_id):

        for person in item['overall_officials'] or []:

            # TODO: get more information
            if person.get('role', None) != 'Principal Investigator':
                continue

            person_id = helpers.upsert(db['persons'], ['name'], {
                'name': person['last_name'],
                'type': None,
                'data': {},
            })

            helpers.upsert(db['trials_persons'], ['trial_id', 'person_id'], {
                'trial_id': trial_id,
                'person_id': person_id,
                'role': 'principal_investigator',
                'context': {},
            }, auto_id=False)


if __name__ == '__main__':

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    mapper = NctMapper(warehouse, database)
    mapper.map()
