# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'actrn',
        'name': 'ANZCTR',
        'type': 'register',
        'url': 'http://www.anzctr.org.au',
        'terms_and_conditions_url': 'http://www.anzctr.org.au/Support/Terms.aspx',
    }
    return source


def extract_trial(record):

    # Get identifiers
    source_id = 'actrn'
    identifier = record['trial_id']
    if identifier.startswith('NCT'):
        source_id = 'nct'
    identifiers = base.helpers.get_cleaned_identifiers({
        source_id: identifier,
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['public_title'],
        record['scientific_title'],
        record['trial_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Closed: follow-up complete': ['complete', 'not_recruiting'],
        'Closed: follow-up continuing': ['ongoing', 'not_recruiting'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Withdrawn': ['withdrawn', 'not_recruiting'],
        'Stopped early': ['terminated', 'not_recruiting'],
    }
    status, recruitment_status = statuses[record.get('recruitment_status')]

    # Get gender
    gender = None
    if record['gender']:
        if record['gender'].startswith('Both'):
            gender = 'both'
        elif record['gender'].startswith('Male'):
            gender = 'male'
        elif record['gender'].startswith('Female'):
            gender = 'female'

    # Get has_published_results
    has_published_results = None

    trial = {
        'identifiers': identifiers,
        'registration_date': record['date_registered'],
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['scientific_title'],
        'description': record['brief_summary'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'inclusion': record['key_inclusion_criteria'],
            'exclusion': record['key_exclusion_criteria'],
        },
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': record['anticipated_date_of_first_participant_enrolment'],
        'study_type': record['study_type'],
        'study_phase': record['phase'],
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    conditions.append({
        'name': record['health_conditions_or_problems_studied'],
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
    for element in record['sponsors'] or []:
        organisations.append({
            'name': element.get('name', None),
            # ---
            'trial_role': 'sponsor',
        })
    return organisations


def extract_persons(record):
    persons = []
    for role in ['public_queries', 'scientific_queries']:
        persons.append({
            'name': record[role].get('name', None),
            # ---
            'trial_id': record['trial_id'],
            'trial_role': role,
        })
    return persons
