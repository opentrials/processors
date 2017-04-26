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
        'id': 'takeda',
        'name': 'Takeda',
        'type': 'register',
        'source_url': 'http://www.takedaclinicaltrials.com/',
        'terms_and_conditions_url': 'http://www.takedaclinicaltrials.com/legal/terms',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_identifiers({
        'nct': record['nct_number'],
        'takeda': 'TAKEDA-%s' % record['takeda_trial_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['official_title'],
        record['takeda_trial_id'],
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Active not recruiting': ['ongoing', 'not_recruiting'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Status': ['other', 'other'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Withdrawn': ['withdrawn', 'not_recruiting'],
    }
    status, recruitment_status = statuses[record.get('recruitment_status')]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['download_the_clinical_trial_summary']:
        has_published_results = True

    # Get study_phase
    study_phase = base.normalizers.get_normalized_phase(record['trial_phase'])

    # Get age_range
    age_range = _extract_age_range(record)

    return {
        'identifiers': identifiers,
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['eligibility_criteria']},
        'first_enrollment_date': record['start_date'],
        'study_type': record['trial_type'],
        'study_design': record['trial_design'],
        'study_phase': study_phase,
        'gender': gender,
        'age_range': age_range,
        'has_published_results': has_published_results,
    }


def extract_conditions(record):
    conditions = []
    conditions.append({
        'name': record['condition'],
    })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['compound'] or []:
        interventions.append({
            'name': element,
        })
    return interventions


def extract_locations(record):
    locations = []
    for name in record['locations'] or []:
        # For strange case "Republic of"
        if name.strip().lower() == 'republic of':
            continue
        locations.append({
            'name': name,
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


def extract_documents(record):
    documents = []
    results_url = record.get('download_the_clinical_trial_summary')
    if results_url:
        document = {
            'name': 'Results',
            'source_url': results_url,
        }
        documents.append(document)
    return documents


def extract_document_category(record):
    return base.config.DOCUMENT_CATEGORIES['clinical_study_report_synopsis']


def _extract_age_range(record):
    age = (record.get('ages') or '').strip().lower()
    min_age, max_age = None, None
    if age.endswith(' and up'):
        min_age = age[:-len(' and up')]
        max_age = 'no limit'
    elif age.startswith('up to '):
        min_age = 'no limit'
        max_age = age[len('up to '):]
    elif len(re.split('\s*-\s*', age)) == 2:
        min_age, max_age = re.split('\s*-\s*', age)

    return {
        'min_age': base.helpers.format_age(min_age),
        'max_age': base.helpers.format_age(max_age),
    }
