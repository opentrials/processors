# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(item):
    source = {
        'name': 'nct',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(item):
    trial = {
        'identifiers': [item['nct_id']],
        'primary_register': 'nct',
        'primary_id': item['nct_id'],
        'secondary_ids': {'others': item['secondary_ids'] },
        'registration_date': item['firstreceived_date'],
        'public_title': item['brief_title'],
        'brief_summary': item['brief_summary'] or '',  # TODO: review
        'scientific_title': item['official_title'],
        'description': item['detailed_description'],
        'recruitment_status': item['overall_status'],
        'eligibility_criteria': item['eligibility'],
        'target_sample_size': item['enrollment_anticipated'],
        'first_enrollment_date': item['start_date'],
        'study_type': item['study_type'],
        'study_design': item['study_design'],
        'study_phase': item['phase'],
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['secondary_outcomes'] or [],
    }
    return trial


def extract_problems(item):
    problems = []
    for element in item['conditions'] or []:
        problems.append({
            'name': element,
            'type': None,
            'data': {},
            'role': None,
            'context': {},
        })
    return problems


def extract_interventions(item):
    interventions = []
    for element in item['interventions'] or []:
        interventions.append({
            'name': element['intervention_name'],
            'type': None,
            'data': {},
            'role': None,
            'context': element,
        })
    return interventions


def extract_locations(item):
    locations = []
    for element in item['location_countries'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            'data': {},
            'role': 'recruitment_countries',
            'context': {},
        })
    return locations


def extract_organisations(item):
    organisations = []
    for element in item['sponsors'] or []:
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


def extract_persons(item):
    persons = []
    for element in item['overall_officials'] or []:
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
