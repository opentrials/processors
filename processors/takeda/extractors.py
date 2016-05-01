# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime


# Module API

def extract_source(record):
    source = {
        'name': 'takeda',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):
    # TODO: fix
    registration_date = (
        record['start_date'] or datetime.datetime.now().date())
    trial = {
        'identifiers': [record['nct_number']],
        'primary_register': 'takeda',
        'primary_id': record['takeda_trial_id'],
        'secondary_ids': {'nct': record['nct_number']},
        'registration_date': registration_date,  # TODO: review
        'public_title': record['official_title'],  # TODO: review
        'brief_summary': record['brief_summary'] or '',  # TODO: review
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'recruitment_status': record['recruitment_status'],
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'target_sample_size': None,
        'first_enrollment_date': record['start_date'],
        'study_type': record['trial_type'] or 'N/A',  # TODO: review
        'study_design': record['trial_design'] or 'N/A',  # TODO: review
        'study_phase': record['trial_phase'] or 'N/A',  # TODO: review
        'primary_outcomes': None,  # TODO: review free text
        'secondary_outcomes': None,  # TODO: review free text
    }
    return trial


def extract_problems(record):
    problems = []
    problems.append({
        'name': record['condition'],
        'type': 'condition',
        'data': {},
        'role': None,
        'context': {},
    })
    return problems


def extract_interventions(record):
    interventions = []
    for element in record['compound'] or []:
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
    for element in record['locations'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            'data': {},
            'role': 'recruitment_countries',
            'context': {},
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
