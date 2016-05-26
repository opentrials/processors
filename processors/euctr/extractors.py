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
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'who': record['who_universal_trial_reference_number_utrn'],
        'nct': record['us_nct_clinicaltrials_gov_registry_number'],
        'euctr': record['eudract_number_with_country'],
        'isrctn': record['isrctn_international_standard_randomised_controlled_trial_numbe'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['title_of_the_trial_for_lay_people_in_easily_understood_i_e_non_'],
        record['full_title_of_the_trial'],
        record['eudract_number_with_country'])

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
        'primary_id': record['eudract_number_with_country'],
        'identifiers': identifiers,
        'registration_date': record['date_on_which_this_record_was_first_entered_in_the_eudract_data'],
        'public_title': public_title,
        'brief_summary': record['trial_main_objective_of_the_trial'],
        'scientific_title': record['full_title_of_the_trial'],
        'description': record['trial_main_objective_of_the_trial'],
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'inclusion': record['trial_principal_inclusion_criteria'],
            'exclusion': record['trial_principal_exclusion_criteria'],
        },
        'target_sample_size': record['subject_in_the_whole_clinical_trial'],
        'first_enrollment_date': None,
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    if record['trial_medical_condition_s_being_investigated']:
        conditions.append({
            'name': record['trial_medical_condition_s_being_investigated'],
        })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['imps'] or []:
        if 'product_name' not in element:
            continue
        interventions.append({
            'name': element['product_name'],
        })
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    for element in record['sponsors'] or []:
        if 'name_of_sponsor' not in element:
            continue
        organisations.append({
            'name': element['name_of_sponsor'],
            # ---
            'trial_role': 'sponsor',
        })
    return organisations


def extract_persons(record):
    persons = []
    return persons
