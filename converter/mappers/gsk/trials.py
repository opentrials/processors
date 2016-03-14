# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_trials():

    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'gsk',
        'primary_id': item['study_id'],
        'secondary_ids': {
            'nct': item['clinicaltrialsgov_identifier'],
            'others': item['secondary_ids'],
        },
        'registration_date': item['first_received'],  # TODO: review
        'public_title': item['study_title'],
        'brief_summary': item['brief_summary'] or '',  # TODO: review
        'scientific_title': item['official_study_title'],  # TODO: review
        'description': item['detailed_description'],

        # Recruitment
        'recruitment_status': item['study_recruitment_status'],
        'eligibility_criteria': {
            'criteria': item['eligibility_criteria'],  # TODO: bad text - fix on scraper
        },
        'target_sample_size': item['enrollment'],  # TODO: review
        'first_enrollment_date': item['study_start_date'],

        # Study design
        'study_type': item['study_type'],  # TODO: review
        'study_design': item['study_design'] or 'N/A',  # TODO: review
        'study_phase': item['phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['secondary_outcomes'] or [],

    })
