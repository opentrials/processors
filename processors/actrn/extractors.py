# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'name': 'actrn',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get gender
    gender = None
    if record['gender']:
        if record['gender'].startswith('Both'):
            gender = 'both'
        elif record['gender'].startswith('Male'):
            gender = 'male'
        elif record['gender'].startswith('Female'):
            gender = 'female'

    # Get has_published_results
    has_published_results = None

    trial = {
        'identifiers': [],
        'primary_register': 'actrn',
        'primary_id': record['trial_id'],
        'secondary_ids': {
            'others': record['secondary_ids'],
        },
        'registration_date': record['date_registered'],
        'public_title': record['public_title'],
        'brief_summary': record['brief_summary'],
        'scientific_title': record['scientific_title'],
        'description': None,  # TODO: review
        'recruitment_status': record['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': record['key_inclusion_criteria'],
            'exclusion': record['key_exclusion_criteria'],
        },
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': record['anticipated_date_of_first_participant_enrolment'],  # TODO: review
        'study_type': record['study_type'],
        'study_design': 'N/A',  # TODO: review
        'study_phase': record['phase'] or 'N/A',  # TODO: review
        'primary_outcomes': record['primary_outcomes'] or [],
        'secondary_outcomes': record['secondary_outcomes'] or [],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_problems(record):
    # TODO: record['health_conditions_or_problems_studied'] - free text some time
    problems = []
    return problems


def extract_interventions(record):
    # TODO: record['intervention_codes'] - discover
    interventions = []
    return interventions


def extract_locations(record):
    # TODO: no recruitment countries
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        # TODO: process record['primary_sponsor']
        if 'name' not in element:
            continue
        organisations.append({
            'name': element['name'],
            'type': None,
            'data': {},
            'role': 'sponsor',  # TODO: review
            'context': element,
        })
    return organisations


def extract_persons(record):
    persons = []
    # TODO: process record['principal_investigator']
    for role in ['public_queries', 'scientific_queries']:
        persons.append({
            'name': record[role]['name'],
            'type': None,
            'data': {},
            'role': role,
            'context': record[role],
            'phones': [],
        })
    return persons
