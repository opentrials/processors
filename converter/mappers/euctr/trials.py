# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_trials():

    # Log processed item
    print('Processing: %s' % item['eudract_number_with_country'])

    # Create mapping
    mapping = OrderedDict()
    mapping['isrctn_id'] = None
    mapping['euctr_id'] = item['eudract_number']
    mapping['isrctn_id'] = None
    mapping['scientific_title'] = item['full_title_of_the_trial']

    helpers.update_trial(
        conn=wh,
        mapping=mapping,
        identifier='euctr::%s' % item['meta_uuid'])

    # trials

    trial_id = upsert(db['trials'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'euctr',
        'primary_id': item['eudract_number_with_country'],
        'secondary_ids': {
            'nct': item['us_nct_clinicaltrialsgov_registry_number'],
            'who': item['who_universal_trial_reference_number_utrn'],
            'isrctn': item['isrctn_international_standard_randomised_controlled_trial_numbe'],  # TODO: why number, scraper has number
        },
        'registration_date': item['date_on_which_this_record_was_first_entered'],
        'public_title': item['title_of_the_trial_for_lay_people_in'] or '',  # TODO: review
        'brief_summary': item['trial_main_objective_of_the_trial'] or '',  # TODO: review
        'scientific_title': item['full_title_of_the_trial'],
        'description': None,  # TODO: review

        # Recruitment
        'recruitment_status': item['trial_status'],  # TODO: review
        'eligibility_criteria': {
            'inclusion': item['trial_principal_inclusion_criteria'],
            'exclusion': item['trial_principal_exclusion_criteria'],
        },
        'target_sample_size': item['subject_in_the_whole_clinical_trial'],  # TODO: review
        'first_enrollment_date': item['date_on_which_this_record_was_first_entered'],  # TODO: fix on scraper level

        # Study design
        # TODO: discover on scraper level
        'study_type': 'N/A',
        'study_design': 'N/A',
        'study_phase': 'N/A',

        # Outcomes
        # TODO: discover on scraper level
        'primary_outcomes': [],
        'secondary_outcomes': [],

    })

