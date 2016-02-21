# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import uuid
import dataset
import sqlalchemy as sa
from dotenv import load_dotenv
load_dotenv('.env')

from . import helpers


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = helpers.upsert(db['source'], ['name', 'type'], {
    'name': 'nct',
    'type': 'register',
    'data': {},
})


for item in wh['nct'].find(_limit=50):
# for item in wh['nct'].find(nct_id='NCT00104572'):
    print('Writing: %s' % item['nct_id'])


    # trial

    trial_uuid = helpers.upsert(db['trial'], ['primary_register', 'primary_id'], {
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


    # record/trial_record

    record_uuid = item['meta_uuid']

    helpers.upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'nct_id': item['nct_id']},  # TODO: serialization issue
    }, auto_uuid=False)

    helpers.upsert(db['trial_record'], ['trial_uuid', 'record_uuid'], {
        'trial_uuid': trial_uuid,
        'record_uuid': record_uuid,
        'role': 'primary',
        'context': {},
    }, auto_uuid=False)


    # publication/trial_publication

    # ...


    # document/trial_document

    # ...


    # problem/trial_problem

    for condition in item['conditions'] or []:

        problem_uuid = helpers.upsert(db['problem'], ['name', 'type'], {
            'name': condition,
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trial_problem'], ['trial_uuid', 'problem_uuid'], {
            'trial_uuid': trial_uuid,
            'problem_uuid': problem_uuid,
            'role': None,
            'context': {},
        }, auto_uuid=False)


    # intervention/trial_intervention

    for intervention in item['interventions'] or []:

        intervention_uuid = helpers.upsert(db['intervention'], ['name', 'type'], {
            'name': intervention['intervention_name'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trial_intervention'], ['trial_uuid', 'intervention_uuid'], {
            'trial_uuid': trial_uuid,
            'intervention_uuid': intervention_uuid,
            'role': None,
            'context': intervention,
        }, auto_uuid=False)


    # location/trial_location

    for location in item['location_countries'] or []:

        location_uuid = helpers.upsert(db['location'], ['name', 'type'], {
            'name': location,
            'type': 'country',
            'data': {},
        })

        helpers.upsert(db['trial_location'], ['trial_uuid', 'location_uuid'], {
            'trial_uuid': trial_uuid,
            'location_uuid': location_uuid,
            'role': 'recruitment_countries',
            'context': {},
        }, auto_uuid=False)


    # organisation/trial_organisation

    for sponsor in item['sponsors'] or []:

        # TODO: get more information
        sponsor = sponsor.get('lead_sponsor', None)
        if sponsor is None:
            continue

        organisation_uuid = helpers.upsert(db['organisation'], ['name'], {
            'name': sponsor['agency'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'primary_sponsor',
            'context': {},
        }, auto_uuid=False)


    # person/trial_person

    for person in item['overall_officials'] or []:

        # TODO: get more information
        if person['role'] != 'Principal Investigator':
            continue

        person_uuid = helpers.upsert(db['person'], ['name'], {
            'name': person['last_name'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
            'trial_uuid': trial_uuid,
            'person_uuid': person_uuid,
            'role': 'principal_investigator',
            'context': {},
        }, auto_uuid=False)
