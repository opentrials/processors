# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'takeda',
        'name': 'Takeda',
        'type': 'register',
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
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'first_enrollment_date': record['start_date'],
        'study_type': record['trial_type'],
        'study_design': record['trial_design'],
        'study_phase': record['trial_phase'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    name = base.helpers.clean_string(record['condition'])
    if name:
        conditions.append({
            'name': name,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['compound'] or []:
        name = base.helpers.clean_string(element)
        if name:
            interventions.append({
                'name': name,
            })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['locations'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            # ---
            'trial_role': 'recruitment_countries',
        })
    return locations


def extract_organisations(record):
    organisations = []
    return organisations


def extract_persons(record):
    persons = []
    return persons
