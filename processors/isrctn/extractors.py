# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'isrctn',
        'name': 'ISRCTN',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['clinicaltrialsgov_number'],
        'isrctn': record['isrctn_id'],
    })

    # TODO: review
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
        'primary_register': 'ISRCTN',
        'primary_id': record['isrctn_id'],
        'identifiers': identifiers,
        'registration_date': record['date_applied'],  # TODO: review
        'public_title': record['title'],
        'brief_summary': record['plain_english_summary'],
        'scientific_title': record['scientific_title'],
        'description': None,  # TODO: review
        'recruitment_status': record['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': record['participant_inclusion_criteria'],
            'exclusion': record['participant_exclusion_criteria'],
        },
        'target_sample_size': target_sample_size,
        'first_enrollment_date': record['overall_trial_start_date'],
        'study_type': record['primary_study_design'],
        'study_design': record['study_design'],
        'study_phase': record['phase'] or 'N/A',  # TODO: review
        'primary_outcomes': record['primary_outcome_measures'] or [],
        'secondary_outcomes': record['secondary_outcome_measures'] or [],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    # TODO: record['condition'] - free text
    conditions = []
    return conditions


def extract_interventions(record):
    # TODO: record['interventions'] - free text
    # TODO: record['drug_names'] - free text
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    # TODO: move split to scraper
    for element in (record['countries_of_recruitment'] or '').split(',') or []:
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
        organisations.append({
            'name': element['organisation'],
            'type': None,
            'data': element,
            'context': {},
            # ---
            'trial_role': 'sponsor',
        })
    for element in record['funders'] or []:
        organisations.append({
            'name': element['funder_name'],
            'type': None,
            'data': element,
            'context': {},
            # ---
            'trial_role': 'funder',
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['contacts'] or []:
        # TODO: review
        name = element.get('primary_contact', element.get('additional_contact'))
        if not name:
            continue
        persons.append({
            'name': name,
            'type': None,
            'data': {},
            'context': element,
            'phones': [],
            # ---
            'trial_id': record['isrctn_id'],
            'trial_role': None,
        })
    return persons
