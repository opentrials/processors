# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_trials():
    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'jprn',
        'primary_id': item['unique_trial_number'],
        'secondary_ids': {},  # TODO: use item['secondary_study_id_*'] and item['org_issuing_secondary_study_id_*']
        'registration_date': item['date_of_registration'],
        'public_title': item['title_of_the_study'],
        'brief_summary': 'N/A',  # TODO: review
        'scientific_title': item['official_scientific_title_of_the_study'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': item['key_inclusion_criteria'],
            'exclusion': item['key_exclusion_criteria'],
        },
        'target_sample_size': item['target_sample_size'],
        'first_enrollment_date': item['anticipated_trial_start_date'],  # TODO: review

        # Study design
        'study_type': item['study_type'] or 'N/A',  # TODO: review
        'study_design': item['basic_design'] or 'N/A',  # TODO: review
        'study_phase': item['developmental_phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['key_secondary_outcomes'] or [],

    })
