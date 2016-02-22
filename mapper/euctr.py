# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import uuid
import dataset
import sqlalchemy as sa
from dotenv import load_dotenv
load_dotenv('.env')

from .helpers import upsert


wh = dataset.connect(os.environ['OPENTRIALS_WAREHOUSE_URL'])
db = dataset.connect(os.environ['OPENTRIALS_DATABASE_URL'])


# source

source_uuid = upsert(db['source'], ['name', 'type'], {
    'name': 'euctr',
    'type': 'register',
    'data': {},
})


for item in wh['euctr'].find(_limit=50):
# for item in wh['euctr'].find(eudract_number_with_country='2010-024332-42-BE'):

    print('Writing: %s' % item['eudract_number_with_country'])

    # trial

    trial_uuid = upsert(db['trial'], ['primary_register', 'primary_id'], {

        # General
        'primary_register': 'euctr',
        'primary_id': item['eudract_number_with_country'],
        'secondary_ids': {
            'nct': item['us_nct_clinicaltrialsgov_registry_number'],
            'who': item['who_universal_trial_reference_number_utrn'],
            'isrctn': item['isrctn_international_standard_randomised_controlled_trial_numbe'],  # TODO: why number, scraper has number
        },
        'registration_date': item['date_on_which_this_record_was_first_entered'],
        'public_title': item['title_of_the_trial_for_lay_people_in'],
        'brief_summary': item['trial_main_objective_of_the_trial'],  # TODO: review
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


    # record/trial_record

    record_uuid = item['meta_uuid']

    upsert(db['record'], ['uuid'], {
        'uuid': record_uuid,
        'source_uuid': source_uuid,
        'type': 'trial',
        'data': {'eudract_number_with_country': item['eudract_number_with_country']},  # TODO: serialization issue
    }, auto_uuid=False)

    upsert(db['trial_record'], ['trial_uuid', 'record_uuid'], {
        'trial_uuid': trial_uuid,
        'record_uuid': record_uuid,
        'role': 'primary',
        'context': {},
    }, auto_uuid=False)


    # publication/trial_publication

    # ...


    # document/trial_document

    # ...


    # problem/trial_problem

    # TODO: discover item['trial_medical_conditions_being_investigated']


    # intervention/trial_intervention

    for intervention in item['imps'] or []:

        if 'product_name' not in intervention:
            continue

        intervention_uuid = upsert(db['intervention'], ['name', 'type'], {
            'name': intervention['product_name'],
            'type': None,
            'data': {},
        })

        upsert(db['trial_intervention'], ['trial_uuid', 'intervention_uuid'], {
            'trial_uuid': trial_uuid,
            'intervention_uuid': intervention_uuid,
            'role': None,
            'context': intervention,
        }, auto_uuid=False)


    # location/trial_location

    # TODO: discover on scraper level


    # organisation/trial_organisation

    for sponsor in item['sponsors'] or []:

        if 'name_of_sponsor' not in intervention:
            continue

        organisation_uuid = upsert(db['organisation'], ['name'], {
            'name': sponsor['name_of_sponsor'],
            'type': None,
            'data': {},
        })

        upsert(db['trial_organisation'], ['trial_uuid', 'organisation_uuid'], {
            'trial_uuid': trial_uuid,
            'organisation_uuid': organisation_uuid,
            'role': 'sponsor',
            'context': sponsor,
        }, auto_uuid=False)


    # person/trial_person

    # TODO: discover on scraper level
