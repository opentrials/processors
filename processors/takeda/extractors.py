# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'takeda',
        'name': 'Takeda',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['nct_number'],
        'takeda': record['takeda_trial_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['official_title'],
        record['takeda_trial_id'])

    # TODO: fix
    # Get registration date
    registration_date = (
        record['start_date'] or datetime.datetime.now().date())

    # Get recruitment status
    statuses = {
        'Active not recruiting': 'other',
        'Completed': 'complete',
        'Enrolling by invitation': 'recruiting',
        'Not yet recruiting': 'pending',
        'Recruiting': 'recruiting',
        'Status': 'other',
        'Terminated': 'other',
        'Withdrawn': 'other',
    }
    recruitment_status = statuses[record['recruitment_status']]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['download_the_clinical_trial_summary']:
        has_published_results = True

    trial = {
        'primary_register': 'Takeda',
        'primary_id': record['takeda_trial_id'],
        'identifiers': identifiers,
        'registration_date': registration_date,  # TODO: review
        'public_title': public_title,
        'brief_summary': record['brief_summary'] or '',  # TODO: review
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'target_sample_size': None,
        'first_enrollment_date': record['start_date'],
        'study_type': record['trial_type'] or 'N/A',  # TODO: review
        'study_design': record['trial_design'] or 'N/A',  # TODO: review
        'study_phase': record['trial_phase'] or 'N/A',  # TODO: review
        'primary_outcomes': None,  # TODO: review free text
        'secondary_outcomes': None,  # TODO: review free text
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    conditions.append({
        'name': record['condition'],
        'data': {},
        'role': None,
        'context': {},
        'description': None,
        'icdcm_code': None,
    })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['compound'] or []:
        interventions.append({
            'name': element,
            'type': None,
            'data': {},
            'role': None,
            'context': {},
            'description': None,
            'icdpcs_code': None,
            'ndc_code': None,
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['locations'] or []:
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
    # TODO: review on scraper level
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: review on scraper level
    persons = []
    return persons
