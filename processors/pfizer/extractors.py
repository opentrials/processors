# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'pfizer',
        'name': 'Pfizer',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['nct_id'],
    })

    # Get recruitment status
    statuses = {
        'Active, not recruiting': 'other',
        'Available': 'recruiting',
        'Completed': 'complete',
        'Enrolling by invitation': 'recruiting',
        'Not yet recruiting': 'pending',
        'Recruiting': 'recruiting',
        'Terminated': 'other',
        'Unknown': 'other',
        'Withdrawn': 'other',
    }
    recruitment_status = statuses[record['status']]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = None

    trial = {
        'primary_register': 'Pfizer',
        'primary_id': record['nct_id'],
        'identifiers': identifiers,
        'registration_date': record['study_start_date'],  # TODO: review
        'public_title': record['title'] or 'N/A',  # TODO: review
        'brief_summary': '',  # TODO: review
        'scientific_title': None,  # TODO: review
        'description': None,  # TODO: review
        'recruitment_status': recruitment_status,
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


def extract_conditions(record):
    # TODO: check on scraper level
    conditions = []
    return conditions


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
