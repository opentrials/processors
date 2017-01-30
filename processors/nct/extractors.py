# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'nct',
        'name': 'ClinicalTrials.gov',
        'type': 'register',
        'source_url': 'https://clinicaltrials.gov',
        'terms_and_conditions_url': 'https://clinicaltrials.gov/ct2/about-site/terms-conditions',
    }
    return source


def extract_trial(record):

    # Get identifiers
    raw_identifiers = {'nct': record['nct_id']}
    for secondary_id in record['secondary_ids'] or []:
        secondary_ids = base.helpers.find_list_of_identifiers(secondary_id)
        [raw_identifiers.update(sec_id) for sec_id in secondary_ids]

    identifiers = base.helpers.clean_identifiers(raw_identifiers)

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['brief_title'],
        record['official_title'],
        record['nct_id']
    )

    # Get status and recruitment status
    statuses = {
        None: [None, None],
        'Unknown status': ['unknown', 'unknown'],
        'Active, not recruiting': ['ongoing', 'not_recruiting'],
        'Approved for marketing': ['other', 'other'],
        'Available': ['ongoing', 'unknown'],
        'Completed': ['complete', 'not_recruiting'],
        'Enrolling by invitation': ['ongoing', 'recruiting'],
        'No longer available': ['other', 'other'],
        'Not yet recruiting': ['ongoing', 'not_recruiting'],
        'Recruiting': ['ongoing', 'recruiting'],
        'Suspended': ['suspended', 'not_recruiting'],
        'Temporarily not available': ['other', 'other'],
        'Terminated': ['terminated', 'not_recruiting'],
        'Withdrawn': ['withdrawn', 'not_recruiting'],
        'Withheld': ['other', 'other'],
    }
    status, recruitment_status = statuses[record.get('overall_status')]

    # Get gender
    gender = None
    if (record['eligibility'] or {}).get('gender'):
        gender = record['eligibility']['gender'].lower()
        if gender == 'all':
            gender = 'both'

    # Get has_published_results
    has_published_results = False
    if record['clinical_results']:
        has_published_results = True

    target_sample_size = record.get('enrollment_anticipated')
    if target_sample_size is None:
        target_sample_size = record.get('enrollment_actual')

    # Get study phase
    study_phase = base.normalizers.get_normalized_phase(record['phase'])

    trial = {
        'identifiers': identifiers,
        'registration_date': record['firstreceived_date'],
        'completion_date': record['completion_date_actual'],
        'last_verification_date': record['verification_date'],
        'public_title': public_title,
        'brief_summary': record['brief_summary'],
        'scientific_title': record['official_title'],
        'description': record['detailed_description'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': record['eligibility'],
        'target_sample_size': target_sample_size,
        'first_enrollment_date': record['start_date'],
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': study_phase,
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
        'results_exemption_date': record['results_exemption_date'],
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
    for element in record['interventions'] or []:
        interventions.append({
            'name': element['intervention_name'],
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['location_countries'] or []:
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
            'name': element.get('lead_spondor', {}).get('agency', ''),
            # ---
            'trial_role': 'primary_sponsor',
        })
    return organisations


def extract_persons(record):
    persons = []
    for element in record['overall_officials'] or []:
        if element.get('role', None) == 'Principal Investigator':
            persons.append({
                'name': element['last_name'],
                # ---
                'trial_id': record['nct_id'],
                'trial_role': 'principal_investigator',
            })
    return persons


def extract_documents(record):
    documents = []
    if record['clinical_results']:
        identifiers = base.helpers.clean_identifiers({
            'nct': record['nct_id'],
        })
        identifier = identifiers['nct']
        document = {
            'name': 'Results',
            'source_url': 'https://clinicaltrials.gov/ct2/show/results/' + identifier,
        }
        documents.append(document)
    return documents


def extract_document_category(record):
    return {
        'id': 22,
        'name': 'Clinical study report',
        'group': 'Results',
    }
