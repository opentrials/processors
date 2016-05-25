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
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['nct_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['brief_title'],
        record['official_title'],
        record['nct_id'])

    # Get recruitment status
    statuses = {
        'Active, not recruiting': 'other',
        'Approved for marketing': 'other',
        'Available': 'recruiting',
        'Completed': 'complete',
        'Enrolling by invitation': 'recruiting',
        'No longer available': 'other',
        'Not yet recruiting': 'pending',
        'Recruiting': 'recruiting',
        'Suspended': 'suspended',
        'Temporarily not available': 'suspended',
        'Terminated': 'other',
        'Withdrawn': 'other',
        'Withheld': 'other',
    }
    recruitment_status = statuses[record['overall_status']]

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
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'recruitment_status': recruitment_status,
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


def extract_conditions(record):
    conditions = []
    for element in record['conditions'] or []:
        conditions.append({
            'name': element,
            'description': None,
            'icdcm_code': None,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['interventions'] or []:
        interventions.append({
            'name': element['intervention_name'],
            'type': None,
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
            # ---
            'trial_role': 'recruitment_countries',
        })
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        element = element.get('lead_sponsor', None)
        if element is None:
            continue
        organisations.append({
            'name': element['agency'],
            # ---
            'trial_role': 'primary_sponsor',
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['overall_officials'] or []:
        if element.get('role', None) != 'Principal Investigator':
            continue
        persons.append({
            'name': element['last_name'],
            'phones': [],
            # ---
            'trial_id': record['nct_id'],
            'trial_role': 'principal_investigator',
        })
    return persons
