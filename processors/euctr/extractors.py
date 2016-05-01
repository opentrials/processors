# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'name': 'euctr',
        'type': 'register',
        'data': {},
    }
    return source


def extract_trial(record):
    trial = {
        'identifiers': [record['eudract_number_with_country']],
        'primary_register': 'euctr',
        'primary_id': record['eudract_number_with_country'],  # TODO: review
        'secondary_ids': {
            'nct': record['us_nct_clinicaltrialsgov_registry_number'],
            'who': record['who_universal_trial_reference_number_utrn'],
            'isrctn': record['isrctn_international_standard_randomised_controlled_trial_numbe'],  # TODO: why number, scraper has number
        },
        'registration_date': record['date_on_which_this_record_was_first_entered'],
        'public_title': record['title_of_the_trial_for_lay_people_in'] or '',  # TODO: review
        'brief_summary': record['trial_main_objective_of_the_trial'] or '',  # TODO: review
        'scientific_title': record['full_title_of_the_trial'],
        'description': None,  # TODO: review
        'recruitment_status': record['trial_status'],  # TODO: review
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
    }
    return trial


def extract_problems(record):
    # TODO: discover record['trial_medical_conditions_being_investigated']
    problems = []
    return problems


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
            'role': 'sponsor',
            'context': element
        })
    return organisations


def extract_persons(record):
    # TODO: discover on scraper level
    persons = []
    return persons
