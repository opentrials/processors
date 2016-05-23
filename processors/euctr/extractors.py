# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'euctr',
        'name': 'EU Clinical Trials Register',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'who': record['who_universal_trial_reference_number_utrn'],
        'nct': record['us_nct_clinicaltrialsgov_registry_number'],
        'euctr': record['eudract_number_with_country'],
        'isrctn': record['isrctn_international_standard_randomised_controlled_trial_numbe']  # TODO: fix on scraper level,
    })

    # Get recruitment status
    statuses = {
        'Completed': 'complete',
        'Not Authorised': 'other',
        'Ongoing': 'recruiting',
        '': 'other',
        'Prematurely Ended': 'other',
        'Prohibited by CA': 'other',
        'Restarted': 'recruiting',
        'Suspended by CA': 'suspended',
        'Temporarily Halted': 'suspended',
    }
    recruitment_status = statuses[record['trial_status']]

    # Get gender
    gender = None
    if record['subject_male'] and record['subject_female']:
        gender = 'both'
    elif record['subject_male']:
        gender = 'male'
    elif record['subject_female']:
        gender = 'female'

    # Get has_published_results
    has_published_results = False
    if record['trial_results'] == 'View results':
        has_published_results = True

    trial = {
        'primary_register': 'EU Clinical Trials Register',
        'primary_id': record['eudract_number_with_country'],  # TODO: review
        'identifiers': identifiers,
        'registration_date': record['date_on_which_this_record_was_first_entered'],
        'public_title': record['title_of_the_trial_for_lay_people_in'] or '',  # TODO: review
        'brief_summary': record['trial_main_objective_of_the_trial'] or '',  # TODO: review
        'scientific_title': record['full_title_of_the_trial'],
        'description': None,  # TODO: review
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'inclusion': record['trial_principal_inclusion_criteria'],
            'exclusion': record['trial_principal_exclusion_criteria'],
        },
        'target_sample_size': record['subject_in_the_whole_clinical_trial'],  # TODO: review
        'first_enrollment_date': record['date_on_which_this_record_was_first_entered'],  # TODO: fix on scraper level
        # TODO: discover on scraper level
        'study_type': 'N/A',
        'study_design': 'N/A',
        'study_phase': 'N/A',
        # TODO: discover on scraper level
        'primary_outcomes': [],
        'secondary_outcomes': [],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    # TODO: discover record['trial_medical_conditions_being_investigated']
    conditions = []
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['imps'] or []:
        if 'product_name' not in element:
            continue
        interventions.append({
            'name': element['product_name'],
            'type': None,
            'data': {},
            'role': None,
            'context': element,
            'description': None,
            'icdpcs_code': None,
            'ndc_code': None,
        })
    return interventions


def extract_locations(record):
    # TODO: discover on scraper level
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        if 'name_of_sponsor' not in element:
            continue
        organisations.append({
            'name': element['name_of_sponsor'],
            'type': None,
            'data': {},
            'context': element,
            # ---
            'trial_role': 'sponsor',
        })
    return organisations


def extract_persons(record):
    # TODO: discover on scraper level
    persons = []
    return persons
