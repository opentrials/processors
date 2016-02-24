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

from ..helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = upsert(db['source'], ['name', 'type'], {
    'name': 'gsk',
    'type': 'register',
    'data': {},
})


for item in wh['gsk'].find(_limit=50):
# for item in wh['gsk'].find(study_id='100181'):

    # TODO: discover on scraper level
    if item['first_received'] is None:
        continue

    print('Writing: %s' % item['study_id'])

    # trial

    trial_uuid = upsert(db['trial'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'gsk',
        'primary_id': item['study_id'],
        'secondary_ids': {
            'nct': item['clinicaltrialsgov_identifier'],
            'others': item['secondary_ids'],
        },
        'registration_date': item['first_received'],  # TODO: review
        'public_title': item['study_title'],
        'brief_summary': item['brief_summary'],
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


    # record/trial_record

    record_uuid = item['meta_uuid']

    upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'study_id': item['study_id']},  # TODO: serialization issue
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

    for condition in item['conditions'] or []:

        problem_uuid = upsert(db['problem'], ['name', 'type'], {
            'name': condition,
            'type': None,
            'data': {},
        })

        upsert(db['trial_problem'], ['trial_uuid', 'problem_uuid'], {
            'trial_uuid': trial_uuid,
            'problem_uuid': problem_uuid,
            'role': None,
            'context': {},
        }, auto_uuid=False)


    # intervention/trial_intervention

    # TODO: item['interventions'] - reimplement on scraper - array -> dict


    # location/trial_location

    # TODO: no recruitment countries field


    # organisation/trial_organisation

    # TODO: discover how to get it/fix it on scraper


    # person/trial_person

    # TODO: discover how to get it/fix it on scraper
