# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'gsk',
        'name': 'GlaxoSmithKline',
        'type': 'register',
        'source_url': 'http://www.gsk.com',
        'terms_and_conditions_url': 'http://www.gsk.com/en-gb/terms-of-use',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_identifiers({
        'nct': record['clinicaltrials_gov_identifier'],
        'gsk': record['study_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['study_title'],
        record['official_study_title'],
        record['study_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Active not recruiting': ['ongoing', 'not_recruiting'],
        'Completed': ['complete', 'not_recruiting'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Withdrawn': ['withdrawn', 'not_recruiting'],
    }
    status, recruitment_status = statuses[record.get('study_recruitment_status')]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['protocol_id']:
        has_published_results = True

    # Get study_phase
    study_phase = base.normalizers.get_normalized_phase(record['phase'])

    trial = {
        'identifiers': identifiers,
        'registration_date': record['first_received'],
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_study_title'],
        'description': record['detailed_description'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'criteria': record['eligibility_criteria'],
        },
        'target_sample_size': record['enrollment'],
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': study_phase,
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
        'last_verification_date': record['record_verification_date'],
    }
    return trial


def extract_conditions(record):
    conditions = []
    for element in record['conditions'] or []:
        conditions.append({
            'name': element,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    return organisations


def extract_persons(record):
    persons = []
    return persons


def extract_documents(record):
    documents = []
    results_url = record.get('results_url')
    if results_url:
        document = {
            'name': 'Results',
            'source_url': results_url,
        }
        documents.append(document)
    return documents


def extract_document_category(record):
    return {
        'id': 22,
        'name': 'Clinical study report',
        'group': 'Results',
    }
