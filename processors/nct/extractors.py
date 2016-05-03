# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'name': 'nct',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get gender
    gender = None
    if record['eligibility'].get('gender', None):
        gender = record['eligibility']['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['clinical_results']:
        has_published_results = True

    trial = {
        'identifiers': [record['nct_id']],
        'primary_register': 'nct',
        'primary_id': record['nct_id'],
        'secondary_ids': {'others': record['secondary_ids']},
        'registration_date': record['firstreceived_date'],
        'public_title': record['brief_title'],
        'brief_summary': record['brief_summary'] or '',  # TODO: review
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'recruitment_status': record['overall_status'],
        'eligibility_criteria': record['eligibility'],
        'target_sample_size': record['enrollment_anticipated'],
        'first_enrollment_date': record['start_date'],
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': record['phase'],
        'primary_outcomes': record['primary_outcomes'] or [],
        'secondary_outcomes': record['secondary_outcomes'] or [],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_problems(record):
    problems = []
    for element in record['conditions'] or []:
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
        interventions.append({
            'name': element['intervention_name'],
            'type': None,
            'data': {},
            'role': None,
            'context': element,
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['location_countries'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            'data': {},
            'role': 'recruitment_countries',
            'context': {},
        })
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        # TODO: get more information
        element = element.get('lead_sponsor', None)
        if element is None:
            continue
        organisations.append({
            'name': element['agency'],
            'type': None,
            'data': {},
            'role': 'primary_sponsor',
            'context': {},
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['overall_officials'] or []:
        # TODO: get more information
        if element.get('role', None) != 'Principal Investigator':
            continue
        persons.append({
            'name': element['last_name'],
            'type': None,
            'data': {},
            'role': 'principal_investigator',
            'context': {},
            'phones': [],
        })
    return persons
