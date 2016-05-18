# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'nct',
        'name': 'ClinicalTrials.gov',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['nct_id'],
    })

    # Get gender
    gender = None
    if record['eligibility'].get('gender', None):
        gender = record['eligibility']['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['clinical_results']:
        has_published_results = True

    trial = {
        'primary_register': 'ClinicalTrials.gov',
        'primary_id': record['nct_id'],
        'identifiers': identifiers,
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
            'description': None,
            'icdcm_code': None,
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
            'description': None,
            'icdpcs_code': None,
            'ndc_code': None,
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['location_countries'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            'data': {},
            'context': {},
            # ---
            'trial_role': 'recruitment_countries',
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
            'context': {},
            # ---
            'trial_role': 'primary_sponsor',
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
            'context': {},
            'phones': [],
            # ---
            'trial_id': record['nct_id'],
            'trial_role': 'principal_investigator',
        })
    return persons
