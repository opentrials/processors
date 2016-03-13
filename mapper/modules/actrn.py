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

from ..helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_id = upsert(db['sources'], ['name', 'type'], {
    'name': 'actrn',
    'type': 'register',
    'data': {},
})


for item in wh['actrn']:

    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

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


    # records/trials_records

    record_id = item['meta_uuid']

    upsert(db['records'], ['id'], {
        'id': record_id,
        'source_id': source_id,
        'type': 'trial',
        'data': {'actrn_id': item['trial_id']},  # TODO: serialization issue
    }, auto_id=False)

    upsert(db['trials_records'], ['trial_id', 'record_id'], {
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

    # TODO: item['health_conditions_or_problems_studied'] - free text some time


    # interventions/trials_interventions

    # TODO: item['intervention_codes'] - discover


    # locations/trials_locations

    # TODO: no recruitment countries


    # organisations/trials_organisations

    for sponsor in item['sponsors'] or []:

        # TODO: process item['primary_sponsor']

        if 'name' not in sponsor:
            continue

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': sponsor['name'],
            'type': None,
            'data': sponsor,
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'sponsor',  # TODO: review
            'context': {},
        }, auto_id=False)


    # persons/trials_persons

    # TODO: process item['principal_investigator']

    person_id = upsert(db['persons'], ['name'], {
        'name': item['public_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'public_queries',
        'context': item['public_queries'],
    }, auto_id=False)

    person_id = upsert(db['persons'], ['name'], {
        'name': item['scientific_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'scientific_queries',
        'context': item['scientific_queries'],
    }, auto_id=False)


    # Log mapping

    print('Mapped: %s' % item['trial_id'])
    time.sleep(0.1)
