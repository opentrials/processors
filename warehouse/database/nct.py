# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import uuid
import dataset
import sqlalchemy as sa

from . import helpers


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = helpers.upsert(db['source'], ['name', 'type'], {
    'name': 'nct',
    'type': 'register',
})


for item in wh['nct'].find(_limit=10):
# for item in wh['nct'].find(nct_id='NCT00104572'):
    print('Writing: %s' % item['nct_id'])


    # trial

    trial_uuid = helpers.upsert(db['trial'], ['primary_register', 'primary_id'], {
        'primary_register': 'nct',
        'primary_id': item['nct_id'],
        'secondary_ids': {}, # TODO: keys issue
        'registration_date': item.get('firstreceived_date'),
        'public_title': item.get('brief_title'),
        'scientific_title': item.get('official_title'),
        'description': item.get('brief_summary'),
        'eligibility_criteria': '', #TODO: merge json
        'target_sample_size': item.get('enrollment_anticipated'),
        'first_enrollment_date': item.get('start_date'),
        'recruitment_status': item.get('overall_status'),
        'study_type': item.get('study_type'),
        'study_design': item.get('study_design'),
        'study_phase': item.get('phase'),
    })


    # trial_outcome

    # ...


    # record/trial_record

    record_uuid = item['meta_uuid']
    helpers.upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'data': {'nct_id': item['nct_id']},  # TODO: serialization issue
    }, auto_uuid=False)
    helpers.upsert(db['trial_record'], ['trial_uuid', 'record_uuid'], {
        'trial_uuid': trial_uuid,
        'record_uuid': record_uuid,
        'role': 'primary',
        'data': {},
    }, auto_uuid=False)


    # problem/trial_problem

    for condition in item.get('conditions', []):
        problem_uuid = helpers.upsert(db['problem'], ['name', 'type'], {
            'name': condition,
            'type': 'condition',
            'data': {},
        })
        helpers.upsert(db['trial_problem'], ['trial_uuid', 'problem_uuid'], {
            'trial_uuid': trial_uuid,
            'problem_uuid': problem_uuid,
            'role': 'studied',
            'data': {},
        }, auto_uuid=False)


    # intervention/trial_intervention

    for intervention in item.get('interventions', []) or []:
        intervention_uuid = helpers.upsert(db['intervention'], ['name', 'type'], {
            'name': intervention['intervention_name'],
            'type': 'drug',
            'data': {},
        })
        helpers.upsert(db['trial_intervention'], ['trial_uuid', 'intervention_uuid'], {
            'trial_uuid': trial_uuid,
            'intervention_uuid': intervention_uuid,
            'role': 'studied',
            'data': intervention,
        }, auto_uuid=False)


    # location/trial_location
    for location in item.get('location_countries', []) or []:
        location_uuid = helpers.upsert(db['location'], ['name', 'type'], {
            'name': location,
            'type': 'country',
            'data': {},
        })
        helpers.upsert(db['trial_location'], ['trial_uuid', 'location_uuid'], {
            'trial_uuid': trial_uuid,
            'location_uuid': location_uuid,
            'role': 'recruitment_countries',
            'data': {},
        }, auto_uuid=False)


    # organisation/trial_organisation

    for sponsor in item.get('sponsors', []) or []:
        # TODO: get more information
        sponsor = sponsor.get('lead_sponsor', None)
        if sponsor is None:
            continue
        organisation_uuid = helpers.upsert(db['organisation'], ['name'], {
            'name': sponsor['agency'],
            'type': 'other',
            'data': {},
        })
        helpers.upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'primary_sponsor',
            'data': {},
        }, auto_uuid=False)


    # person/trial_person

    for person in item.get('overall_officials', []) or []:
        # TODO: get more information
        if person['role'] != 'Principal Investigator':
            continue
        person_uuid = helpers.upsert(db['person'], ['name'], {
            'name': person['last_name'],
            'type': 'other',
            'data': {},
        })
        helpers.upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
            'trial_uuid': trial_uuid,
            'person_uuid': person_uuid,
            'role': 'principal_investigator',
            'data': {},
        }, auto_uuid=False)
