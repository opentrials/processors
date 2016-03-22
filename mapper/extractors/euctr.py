# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


# Module API

class EuctrExtractor(base.Extractor):

    # Public

    store = 'warehouse'
    table = 'data_euctr'

    def extract_source(self, item):

        source = {
            'name': 'euctr',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'euctr_id': item['eudract_number'],
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
            'recruitment_status': item['trial_status'],  # TODO: review
            'eligibility_criteria': {
                'inclusion': item['trial_principal_inclusion_criteria'],
                'exclusion': item['trial_principal_exclusion_criteria'],
            },
            'target_sample_size': item['subject_in_the_whole_clinical_trial'],  # TODO: review
            'first_enrollment_date': item['date_on_which_this_record_was_first_entered'],  # TODO: fix on scraper level
            # TODO: discover on scraper level
            'study_type': 'N/A',
            'study_design': 'N/A',
            'study_phase': 'N/A',
            # TODO: discover on scraper level
            'primary_outcomes': [],
            'secondary_outcomes': [],
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
                'eudract_number_with_country': item['eudract_number_with_country'],
            },
        }

        return record

    def extract_problems(self, item):

        # TODO: discover item['trial_medical_conditions_being_investigated']
        problems = []

        return problems

    def extract_interventions(self, item):

        interventions = []

        for element in item['imps'] or []:

            if 'product_name' not in element:
                continue

            interventions.append({
                'name': element['product_name'],
                'context': element,
            })

        return interventions

    def extract_locations(self, item):

        # TODO: discover on scraper level
        locations = []

        return locations

    def extract_organisations(self, item):

        organisations = []

        for element in item['sponsors'] or []:

            if 'name_of_sponsor' not in element:
                continue

            organisations.append({
                'name': element['name_of_sponsor'],
                'role': 'sponsor',
                'context': element
            })

        return organisations

    def extract_persons(self, item):

        # TODO: discover on scraper level
        persons = []

        return persons
