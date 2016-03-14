# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_trials():

    # Log processed item
    print('Processing: %s' % item['isrctn_id'])

    # Create mapping
    mapping = OrderedDict()
    mapping['nct_id'] = item['clinicaltrialsgov_number']
    mapping['euctr_id'] = None
    mapping['isrctn_id'] = item['isrctn_id']
    mapping['scientific_title'] = item['scientific_title']

    helpers.update_trial(
        conn=wh,
        mapping=mapping,
        identifier='isrctn::%s' % item['meta_uuid'])

    # trials

    # TODO: review
    try:
        target_sample_size = int(item['target_number_of_participants'])

    except Exception:
        target_sample_size = None
    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'isrctn',
        'primary_id': item['isrctn_id'],
        'secondary_ids': {
            'doi_isrctn': item['doi_isrctn_id'],  # TODO: remove isrct part
            'euctr': item['eudract_number'],
            'nct': item['clinicaltrialsgov_number'],
        },
        'registration_date': item['date_applied'],  # TODO: review
        'public_title': item['title'],
        'brief_summary': item['plain_english_summary'],
        'scientific_title': item['scientific_title'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': item['participant_inclusion_criteria'],
            'exclusion': item['participant_exclusion_criteria'],
        },
        'target_sample_size': target_sample_size,
        'first_enrollment_date': item['overall_trial_start_date'],

        # Study design
        'study_type': item['primary_study_design'],
        'study_design': item['study_design'],
        'study_phase': item['phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcome_measures'] or [],
        'secondary_outcomes': item['secondary_outcome_measures'] or [],

    })
