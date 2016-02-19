# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import uuid
import dataset
import sqlalchemy as sa

from .helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = upsert(db['source'], ['name', 'type'], {
    'name': 'isrctn',
    'type': 'register',
    'data': {},
})


for item in wh['isrctn'].find(_limit=50):
# for item in wh['isrctn'].find(isrctn_id='ISRCTN05858391'):
    print('Writing: %s' % item['isrctn_id'])


    # trial

    # TODO: review
    try:
        target_sample_size = int(item['target_number_of_participants'])
    except Exception:
        target_sample_size = None

    trial_uuid = upsert(db['trial'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'isrctn',
        'primary_id': item['isrctn_id'],
        'secondary_ids': {
            'doi_isrctn': item['doi_isrctn_id'],  # TODO: remove isrct part
            'euctr': item['eudract_number'],
            'nct': item['clinicaltrialsgov_number'],
        },
        'registration_date': item['date_applied'],
        'public_title': item['title'],
        'brief_summary': item['plain_english_summary'],
        'scientific_title': item['scientific_title'],
        'description': None,

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
        'study_phase': item['phase'] or 'N/A',

        # Outcomes
        'primary_outcomes': item['primary_outcome_measures'] or [],
        'secondary_outcomes': item['secondary_outcome_measures'] or [],

    })


    # record/trial_record

    record_uuid = item['meta_uuid']

    upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'isrctn_id': item['isrctn_id']},  # TODO: serialization issue
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

    # TODO: item['condition'] - free text


    # intervention/trial_intervention

    # TODO: item['interventions'] - free text
    # TODO: item['drug_names'] - free text


    # location/trial_location

    # TODO move to scraper
    countries = (item['countries_of_recruitment'] or '').split(',') or []

    for country in countries:

        location_uuid = upsert(db['location'], ['name', 'type'], {
            'name': country,
            'type': 'country',
            'data': {},
        })

        upsert(db['trial_location'], ['trial_uuid', 'location_uuid'], {
            'trial_uuid': trial_uuid,
            'location_uuid': location_uuid,
            'role': 'recruitment_countries',
            'context': {},
        }, auto_uuid=False)


    # organisation/trial_organisation

    for sponsor in item['sponsors'] or []:

        organisation_uuid = upsert(db['organisation'], ['name'], {
            'name': sponsor['organisation'],
            'type': None,
            'data': sponsor,
        })

        upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'sponsor',
            'context': {},
        }, auto_uuid=False)

    for funder in item['funders'] or []:

        organisation_uuid = upsert(db['organisation'], ['name'], {
            'name': funder['funder_name'],
            'type': None,
            'data': funder,
        })

        upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'funder',
            'context': {},
        }, auto_uuid=False)


    # person/trial_person

    for person in item['contacts'] or []:

        name = person.get('primary_contact', person.get('additional_contact'))
        if not name:
            continue

        person_uuid = upsert(db['person'], ['name'], {
            'name': name,
            'type': None,
            'data': {},
        })

        upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
            'trial_uuid': trial_uuid,
            'person_uuid': person_uuid,
            'role': None,
            'context': person,
        }, auto_uuid=False)
