# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_trials():

    # # Create mapping
    # mapping = OrderedDict()
    # mapping['nct_id'] = item['nct_id']
    # mapping['euctr_id'] = None
    # mapping['isrctn_id'] = None
    # mapping['scientific_title'] = item['official_title']

    # helpers.update_trial(
        # conn=wh,
        # mapping=mapping,
        # identifier='nct::%s' % item['meta_uuid'])

    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'actrn',
        'primary_id': item['trial_id'],
        'secondary_ids': {
            'others': item['secondary_ids'],
        },
        'registration_date': item['date_registered'],
        'public_title': item['public_title'],
        'brief_summary': item['brief_summary'],
        'scientific_title': item['scientific_title'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['recruitment_status'],
        'eligibility_criteria': {
            'inclusion': item['key_inclusion_criteria'],
            'exclusion': item['key_exclusion_criteria'],
        },
        'target_sample_size': item['target_sample_size'],
        'first_enrollment_date': item['anticipated_date_of_first_participant_enrolment'],  # TODO: review

        # Study design
        'study_type': item['study_type'],
        'study_design': 'N/A',  # TODO: review
        'study_phase': item['phase'] or 'N/A',  # TODO: review

        # Outcomes
        'primary_outcomes': item['primary_outcomes'] or [],
        'secondary_outcomes': item['secondary_outcomes'] or [],

    })
