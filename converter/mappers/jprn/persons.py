# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_persons():
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
