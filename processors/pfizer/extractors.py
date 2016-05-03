# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'name': 'pfizer',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = None

    trial = {
        'identifiers': [record['nct_id']],
        'primary_register': 'pfizer',
        'primary_id': record['nct_id'],
        'secondary_ids': {'nct_id': record['nct_id']},
        'registration_date': record['study_start_date'],  # TODO: review
        'public_title': record['title'] or 'N/A',  # TODO: review
        'brief_summary': '',  # TODO: review
        'scientific_title': None,  # TODO: review
        'description': None,  # TODO: review
        'recruitment_status': record['status'],
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'target_sample_size': None,
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'],
        'study_design': 'N/A',  # TODO: review
        'study_phase': 'N/A',  # TODO: review
        'primary_outcomes': None,  # TODO: review
        'secondary_outcomes': None,  # TODO: review
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_problems(record):
    # TODO: check on scraper level
    problems = []
    return problems


def extract_interventions(record):
    # TODO: check on scraper level
    interventions = []
    return interventions


def extract_locations(record):
    # TODO: check on scraper level
    locations = []
    return locations


def extract_organisations(record):
    # TODO: check on scraper level
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: check on scraper level
    persons = []
    return persons
