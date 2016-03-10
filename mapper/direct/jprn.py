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
    'name': 'jprn',
    'type': 'register',
    'data': {},
})


for item in wh['jprn']:

    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'jprn',
        'primary_id': item['unique_trial_number'],
        'secondary_ids': {},  # TODO: use item['secondary_study_id_*'] and item['org_issuing_secondary_study_id_*']
        'registration_date': item['date_of_registration'],
        'public_title': item['title_of_the_study'],
        'brief_summary': 'N/A',  # TODO: review
        'scientific_title': item['official_scientific_title_of_the_study'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': item['key_inclusion_criteria'],
            'exclusion': item['key_exclusion_criteria'],
        },
        'target_sample_size': item['target_sample_size'],
        'first_enrollment_date': item['anticipated_trial_start_date'],  # TODO: review

        # Study design
        'study_type': item['study_type'] or 'N/A',  # TODO: review
        'study_design': item['basic_design'] or 'N/A',  # TODO: review
        'study_phase': item['developmental_phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['key_secondary_outcomes'] or [],

    })


    # records/trials_records

    record_id = item['meta_uuid']

    upsert(db['records'], ['id'], {
        'id': record_id,
        'source_id': source_id,
        'type': 'trial',
        'data': {'unique_trial_number': item['unique_trial_number']},  # TODO: serialization issue
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

    # TODO: item['condition'] - free text some time


    # interventions/trials_interventions

    # TODO: item['interventions'] - array of free texts


    # locations/trials_locations

    # TODO: fix on scraper item['region'] when possible


    # organisations/trials_organisations

    organisation_id = upsert(db['organisations'], ['name'], {
        'name': item['name_of_primary_sponsor'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
        'trial_id': trial_id,
        'organisation_id': organisation_id,
        'role': 'primary_sponsor',
        'context': {},
    }, auto_id=False)

    organisation_id = upsert(db['organisations'], ['name'], {
        'name': item['source_of_funding'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
        'trial_id': trial_id,
        'organisation_id': organisation_id,
        'role': 'funder',
        'context': {},
    }, auto_id=False)


    # persons/trials_persons

    person_id = upsert(db['persons'], ['name'], {
        'name': item['research_name_of_lead_principal_investigator'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'principal_investigator',
        'context': {
            'research_name_of_lead_principal_investigator': item['research_name_of_lead_principal_investigator'],
            'research_organization': item['research_organization'],
            'research_division_name': item['research_division_name'],
            'research_address': item['research_address'],
            'research_tel': item['research_tel'],
            'research_homepage_url': item['research_homepage_url'],
            'research_email': item['research_email'],
        },
    }, auto_id=False)

    person_id = upsert(db['persons'], ['name'], {
        'name': item['public_name_of_contact_person'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'public_queries',
        'context': {
            'public_name_of_contact_person': item['public_name_of_contact_person'],
            'public_organization': item['public_organization'],
            'public_division_name': item['public_division_name'],
            'public_address': item['public_address'],
            'public_tel': item['public_tel'],
            'public_homepage_url': item['public_homepage_url'],
            'public_email': item['public_email'],
        },
    }, auto_id=False)


    # Log mapping

    print('Mapped: %s' % item['unique_trial_number'])
    time.sleep(0.1)
