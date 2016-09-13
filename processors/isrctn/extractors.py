# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'isrctn',
        'name': 'ISRCTN',
        'type': 'register',
        'url': 'http://www.isrctn.com/',
        'terms_and_conditions_url': 'http://www.isrctn.com/page/terms',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.get_cleaned_identifiers({
        'nct': record['clinicaltrials_gov_number'],
        'isrctn': record['isrctn_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['title'],
        record['scientific_title'],
        record['isrctn_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'No longer recruiting': ['ongoing', 'not_recruiting'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Stopped': ['terminated', 'not_recruiting'],
    }
    status, recruitment_status = statuses[record.get('recruitment_status')]

    # Get target sample size
    try:
        target_sample_size = int(record['target_number_of_participants'])
    except Exception:
        target_sample_size = None

    # Get gender
    gender = None
    if record['gender'] and record['gender'] != 'Not Specified':
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['results_basic_reporting']:
        has_published_results = True

    trial = {
        'identifiers': identifiers,
        'registration_date': record['date_applied'],
        'public_title': public_title,
        'brief_summary': record['plain_english_summary'],
        'scientific_title': record['scientific_title'],
        'description': record['plain_english_summary'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'inclusion': record['participant_inclusion_criteria'],
            'exclusion': record['participant_exclusion_criteria'],
        },
        'target_sample_size': target_sample_size,
        'first_enrollment_date': record['overall_trial_start_date'],
        'study_type': record['primary_study_design'],
        'study_design': record['study_design'],
        'study_phase': record['phase'],
        'primary_outcomes': record['primary_outcome_measures'],
        'secondary_outcomes': record['secondary_outcome_measures'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    conditions.append({
        'name': record['condition'],
    })
    return conditions


def extract_interventions(record):
    interventions = []
    if record['drug_names']:
        pattern = r'(?:,)|(?:\d+\.)'
        for element in re.split(pattern, record['drug_names']):
            interventions.append({
                'name': element,
                'type': 'drug',
            })
    return interventions


def extract_locations(record):
    locations = []
    for element in (record['countries_of_recruitment'] or '').split(',') or []:
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
        organisations.append({
            'name': element['organisation'],
            # ---
            'trial_role': 'sponsor',
        })
    for element in record['funders'] or []:
        organisations.append({
            'name': element['funder_name'],
            # ---
            'trial_role': 'funder',
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['contacts'] or []:
        persons.append({
            'name': element.get('primary_contact', element.get('additional_contact')),
            # ---
            'trial_id': record['isrctn_id'],
        })
    return persons
