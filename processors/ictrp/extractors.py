# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime


# Module API

def extract_source(record):
    source = {
        'name': 'ictrp',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    nct_id = None
    euctr_id = None
    isrctn_id = None
    if record['register'] == 'ClinicalTrials.gov':
        nct_id = record['main_id']
    if record['register'] == 'EUCTR':
        euctr_id = record['main_id']
    if record['register'] == 'ISRCTN':
        isrctn_id = record['main_id']

    # TODO: fix
    # Get registration date
    registration_date = datetime.datetime.now().date()

    # Get gender
    gender = None

    # Get has_published_results
    has_published_results = None

    trial = {
        'identifiers': [nct_id, euctr_id, isrctn_id],
        'primary_register': 'ictrp',
        'primary_id': record['main_id'],
        'secondary_ids': {},
        'registration_date': registration_date,  # TODO: text on scrap layer
        'public_title': record['public_title'],
        'brief_summary': '',  # TODO: review
        'scientific_title': record['scientific_title'],  # TODO: review
        'description': None,  # TODO: review
        'recruitment_status': record['recruitment_status'],
        'eligibility_criteria': {'criteria': record['key_inclusion_exclusion_criteria']},
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': None,  # TODO: text on scraper layer
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': record['study_phase'] or 'N/A',
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_problems(record):
    problems = []
    for element in record['health_conditions_or_problems_studied'] or []:
        problems.append({
            'name': element,
            'type': None,
            'data': {},
            'role': None,
            'context': {},
        })
    return problems


def extract_interventions(record):
    interventions = []
    for element in record['interventions'] or []:
        # TODO: parse "drug: name"
        interventions.append({
            'name': element,
            'type': None,
            'data': {},
            'role': None,
            'context': {},
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['countries_of_recruitment'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            'data': {},
            'role': 'recruitment_countries',
            'context': {},
        })
    return locations


def extract_organisations(record):
    # TODO: check on scraper level
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: check on scraper level
    persons = []
    return persons
