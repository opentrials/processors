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

from .helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = upsert(db['source'], ['name', 'type'], {
    'name': 'actrn',
    'type': 'register',
    'data': {},
})


for item in wh['actrn'].find(_limit=50):
# for item in wh['actrn'].find(trial_id='ACTRN12615000001594'):
    print('Writing: %s' % item['trial_id'])


    # trial

    trial_uuid = upsert(db['trial'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'actrn',
        'primary_id': item['trial_id'],
        'secondary_ids': {
            'others': item['secondary_ids'],
        },
        'registration_date': item['date_registered'],
        'public_title': item['public_title'],
        'brief_summary': item['brief_summary'],
        'scientific_title': item['scientific_title'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': item['key_inclusion_criteria'],
            'exclusion': item['key_exclusion_criteria'],
        },
        'target_sample_size': item['target_sample_size'],
        'first_enrollment_date': item['anticipated_date_of_first_participant_enrolment'],  # TODO: review

        # Study design
        'study_type': item['study_type'],
        'study_design': 'N/A',  # TODO: review
        'study_phase': item['phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['secondary_outcomes'] or [],

    })


    # record/trial_record

    record_uuid = item['meta_uuid']

    upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'actrn_id': item['trial_id']},  # TODO: serialization issue
    }, auto_uuid=False)

    upsert(db['trial_record'], ['trial_uuid', 'record_uuid'], {
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

    # TODO: item['health_conditions_or_problems_studied'] - free text some time


    # intervention/trial_intervention

    # TODO: item['intervention_codes'] - discover


    # location/trial_location

    # TODO: no recruitment countries


    # organisation/trial_organisation

    for sponsor in item['sponsors'] or []:

        # TODO: process item['primary_sponsor']

        if 'name' not in sponsor:
            continue

        organisation_uuid = upsert(db['organisation'], ['name'], {
            'name': sponsor['name'],
            'type': None,
            'data': sponsor,
        })

        upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'sponsor',  # TODO: review
            'context': {},
        }, auto_uuid=False)


    # person/trial_person

    # TODO: process item['principal_investigator']

    person_uuid = upsert(db['person'], ['name'], {
        'name': item['public_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
        'trial_uuid': trial_uuid,
        'person_uuid': person_uuid,
        'role': 'public_queries',
        'context': item['public_queries'],
    }, auto_uuid=False)

    person_uuid = upsert(db['person'], ['name'], {
        'name': item['scientific_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
        'trial_uuid': trial_uuid,
        'person_uuid': person_uuid,
        'role': 'scientific_queries',
        'context': item['scientific_queries'],
    }, auto_uuid=False)
