# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime


# Module API

def extract_source(record):
    source = {
        'id': 'gsk',
        'name': 'GlaxoSmithKline',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # TODO: fix
    # Get registration date
    registration_date = (
        record['first_received'] or datetime.datetime.now().date())

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['protocol_id']:
        has_published_results = True

    trial = {
        'identifiers': [record['clinicaltrialsgov_identifier']],
        'primary_register': 'GlaxoSmithKline',
        'primary_id': record['study_id'],
        'secondary_ids': {
            'nct': record['clinicaltrialsgov_identifier'],
            'others': record['secondary_ids'],
        },
        'registration_date': registration_date,  # TODO: review
        'public_title': record['study_title'],
        'brief_summary': record['brief_summary'] or '',  # TODO: review
        'scientific_title': record['official_study_title'],  # TODO: review
        'description': record['detailed_description'],
        'recruitment_status': record['study_recruitment_status'],
        'eligibility_criteria': {
            'criteria': record['eligibility_criteria'],  # TODO: bad text - fix on scraper
        },
        'target_sample_size': record['enrollment'],  # TODO: review
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'] or 'N/A',  # TODO: review
        'study_design': record['study_design'] or 'N/A',  # TODO: review
        'study_phase': record['phase'] or 'N/A',  # TODO: review
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
    # TODO: record['interventions'] - reimplement on scraper - array -> dict
    interventions = []
    return interventions


def extract_locations(record):
    # TODO: no recruitment countries field
    locations = []
    return locations


def extract_organisations(record):
    # TODO: discover how to get it/fix it on scraper
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: discover how to get it/fix it on scraper
    persons = []
    return persons
