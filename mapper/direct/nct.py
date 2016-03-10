# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset
from dotenv import load_dotenv
load_dotenv('.env')

from .. import helpers


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_id = helpers.upsert(db['sources'], ['name', 'type'], {
    'name': 'nct',
    'type': 'register',
    'data': {},
})


offset = 0
while True:

    # Get items
    query = {'_offset': offset, '_limit': 10, 'order_by': 'meta_uuid'}
    count = wh['nct'].find(return_count=True, **query)
    if not count:
        break
    items = wh['nct'].find(**query)
    offset += 10

    for item in items:

        # trials

        trial_id = helpers.upsert(db['trials'], ['primary_register', 'primary_id'], {
            'primary_register': 'nct',
            'primary_id': item['nct_id'],
            'secondary_ids': {'others': item['secondary_ids'] },
            'registration_date': item['firstreceived_date'],
            'public_title': item['brief_title'],
            'brief_summary': item['brief_summary'],
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


        # records/trials_records

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


        # publications/trials_publications

        # ...


        # documents/trials_documents

        # ...


        # problems/trials_problems

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


        # interventions/trials_interventions

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


        # locations/trials_locations

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


        # organisations/trials_organisations

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


        # persons/trials_persons

        for person in item['overall_officials'] or []:

            # TODO: get more information
            if person['role'] != 'Principal Investigator':
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


        # Log mapping
        print('Mapped: %s' % item['nct_id'])
        time.sleep(0.1)
