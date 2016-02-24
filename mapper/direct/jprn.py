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
    'name': 'jprn',
    'type': 'register',
    'data': {},
})


for item in wh['jprn'].find(_limit=50):
# for item in wh['jprn'].find(unique_trial_number='UMIN000006808'):
    print('Writing: %s' % item['unique_trial_number'])


    # trial

    trial_uuid = upsert(db['trial'], ['primary_register', 'primary_id'], {

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


    # record/trial_record

    record_uuid = item['meta_uuid']

    upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'unique_trial_number': item['unique_trial_number']},  # TODO: serialization issue
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

    # TODO: item['condition'] - free text some time


    # intervention/trial_intervention

    # TODO: item['interventions'] - array of free texts


    # location/trial_location

    # TODO: fix on scraper item['region'] when possible


    # organisation/trial_organisation

    organisation_uuid = upsert(db['organisation'], ['name'], {
        'name': item['name_of_primary_sponsor'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
        'trial_uuid': trial_uuid,
        'organisation_uuid': organisation_uuid,
        'role': 'primary_sponsor',
        'context': {},
    }, auto_uuid=False)

    organisation_uuid = upsert(db['organisation'], ['name'], {
        'name': item['source_of_funding'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
        'trial_uuid': trial_uuid,
        'organisation_uuid': organisation_uuid,
        'role': 'funder',
        'context': {},
    }, auto_uuid=False)


    # person/trial_person

    person_uuid = upsert(db['person'], ['name'], {
        'name': item['research_name_of_lead_principal_investigator'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
        'trial_uuid': trial_uuid,
        'person_uuid': person_uuid,
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
    }, auto_uuid=False)

    person_uuid = upsert(db['person'], ['name'], {
        'name': item['public_name_of_contact_person'],
        'type': None,
        'data': {},
    })

    upsert(db['trial_person'], ['trial_uuid', 'person_uuid'], {
        'trial_uuid': trial_uuid,
        'person_uuid': person_uuid,
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
    }, auto_uuid=False)
