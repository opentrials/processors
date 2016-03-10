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
    'name': 'isrctn',
    'type': 'register',
    'data': {},
})


for item in wh['isrctn']:

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


    # records/trials_records

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


    # publications/trials_publications

    # ...


    # documents/trials_documents

    # ...


    # problems/trials_problems

    # TODO: item['condition'] - free text


    # interventions/trials_interventions

    # TODO: item['interventions'] - free text
    # TODO: item['drug_names'] - free text


    # locations/trials_locations

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


    # organisations/trials_organisations

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


    # persons/trials_persons

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


    # Log mapping

    print('Mapped: %s' % item['isrctn_id'])
    time.sleep(0.1)
