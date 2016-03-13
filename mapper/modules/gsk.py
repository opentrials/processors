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
    'name': 'gsk',
    'type': 'register',
    'data': {},
})


for item in wh['gsk']:

    # TODO: discover on scraper level
    if item['first_received'] is None:
        continue

    # trials

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


    # records/trials_records

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


    # publications/trials_publications

    # ...


    # documents/trials_documents

    # ...


    # problems/trials_problems

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


    # interventions/trials_interventions

    # TODO: item['interventions'] - reimplement on scraper - array -> dict


    # locations/trials_locations

    # TODO: no recruitment countries field


    # organisations/trials_organisations

    # TODO: discover how to get it/fix it on scraper


    # persons/trials_persons

    # TODO: discover how to get it/fix it on scraper


    # Log mapping

    print('Mapped: %s' % item['study_id'])
    time.sleep(0.1)
