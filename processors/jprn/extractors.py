# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'name': 'jprn',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):
    trial = {
        'identifiers': [],
        'primary_register': 'jprn',
        'primary_id': record['unique_trial_number'],
        'secondary_ids': {},  # TODO: use record['secondary_study_id_*'] and record['org_issuing_secondary_study_id_*']
        'registration_date': record['date_of_registration'],
        'public_title': record['title_of_the_study'],
        'brief_summary': 'N/A',  # TODO: review
        'scientific_title': record['official_scientific_title_of_the_study'],
        'description': None,  # TODO: review
        'recruitment_status': record['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': record['key_inclusion_criteria'],
            'exclusion': record['key_exclusion_criteria'],
        },
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': record['anticipated_trial_start_date'],  # TODO: review
        'study_type': record['study_type'] or 'N/A',  # TODO: review
        'study_design': record['basic_design'] or 'N/A',  # TODO: review
        'study_phase': record['developmental_phase'] or 'N/A',  # TODO: review
        'primary_outcomes': record['primary_outcomes'] or [],
        'secondary_outcomes': record['key_secondary_outcomes'] or [],
    }
    return trial


def extract_problems(record):
    # TODO: record['condition'] - free text some time
    problems = []
    return problems


def extract_interventions(record):
    # TODO: record['interventions'] - array of free texts
    interventions = []
    return interventions


def extract_locations(record):
    # TODO: fix on scraper record['region'] when possible
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    organisations.append({
        'name': record['name_of_primary_sponsor'],
        'type': None,
        'data': {},
        'role': 'primary_sponsor',
        'context': {},
    })
    organisations.append({
        'name': record['source_of_funding'],
        'type': None,
        'data': {},
        'role': 'funder',
        'context': {},
    })
    return organisations


def extract_persons(record):
    persons = []
    if record['research_name_of_lead_principal_investigator']:
        persons.append({
            'name': record['research_name_of_lead_principal_investigator'],
            'type': None,
            'data': {},
            'role': 'principal_investigator',
            'context': {
                'research_name_of_lead_principal_investigator': record['research_name_of_lead_principal_investigator'],
                'research_organization': record['research_organization'],
                'research_division_name': record['research_division_name'],
                'research_address': record['research_address'],
                'research_tel': record['research_tel'],
                'research_homepage_url': record['research_homepage_url'],
                'research_email': record['research_email'],
            },
            'phones': [],
        })
    if record['public_name_of_contact_person']:
        persons.append({
            'name': record['public_name_of_contact_person'],
            'role': 'public_queries',
            'type': None,
            'data': {},
            'context': {
                'public_name_of_contact_person': record['public_name_of_contact_person'],
                'public_organization': record['public_organization'],
                'public_division_name': record['public_division_name'],
                'public_address': record['public_address'],
                'public_tel': record['public_tel'],
                'public_homepage_url': record['public_homepage_url'],
                'public_email': record['public_email'],
            },
            'phones': [],
        })
    return persons
