# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import time
import dataset
from dotenv import load_dotenv
load_dotenv('.env')

from ..helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# sources

source_id = upsert(db['sources'], ['name', 'type'], {
    'name': 'euctr',
    'type': 'register',
    'data': {},
})


for item in wh['euctr']:

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


    # records/trials_records

    record_id = item['meta_uuid']

    upsert(db['records'], ['id'], {
        'id': record_id,
        'source_id': source_id,
        'type': 'trial',
        'data': {'eudract_number_with_country': item['eudract_number_with_country']},  # TODO: serialization issue
    }, auto_id=False)

    upsert(db['trials_records'], ['trial_id', 'record_id'], {
        'trial_id': trial_id,
        'record_id': record_id,
        'role': 'primary',
        'context': {},
    }, auto_id=False)


    # publications/trials_publications

    # ...


    # documents/trials_documents

    # ...


    # problems/trials_problems

    # TODO: discover item['trial_medical_conditions_being_investigated']


    # interventions/trials_interventions

    for intervention in item['imps'] or []:

        if 'product_name' not in intervention:
            continue

        intervention_id = upsert(db['interventions'], ['name', 'type'], {
            'name': intervention['product_name'],
            'type': None,
            'data': {},
        })

        upsert(db['trials_interventions'], ['trial_id', 'intervention_id'], {
            'trial_id': trial_id,
            'intervention_id': intervention_id,
            'role': None,
            'context': intervention,
        }, auto_id=False)


    # locations/trials_locations

    # TODO: discover on scraper level


    # organisations/trials_organisations

    for sponsor in item['sponsors'] or []:

        if 'name_of_sponsor' not in intervention:
            continue

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': sponsor['name_of_sponsor'],
            'type': None,
            'data': {},
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'sponsor',
            'context': sponsor,
        }, auto_id=False)


    # persons/trials_persons

    # TODO: discover on scraper level


    # Log mapping

    print('Mapped: %s' % item['eudract_number_with_country'])
    time.sleep(0.1)
