# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import datetime

from . import base
logger = logging.getLogger(__name__)


# Module API

class TakedaExtractor(base.Extractor):

    # Public

    store = 'warehouse'
    table = 'takeda'
    heads = ['nct', 'euctr', 'isrctn']

    def extract_source(self, item):

        source = {
            'name': 'takeda',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        # TODO: fix
        registration_date = (
            item['start_date'] or datetime.datetime.now().date())

        trial = {
            'nct_id': item['nct_number'],
            'primary_register': 'takeda',
            'primary_id': item['takeda_trial_id'],
            'secondary_ids': {'nct': item['nct_number']},
            'registration_date': registration_date,  # TODO: review
            'public_title': item['official_title'],  # TODO: review
            'brief_summary': item['brief_summary'] or '',  # TODO: review
            'scientific_title': item['official_title'],
            'description': item['detailed_description'],
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {'criteria': item['eligibility_criteria']},
            'target_sample_size': None,
            'first_enrollment_date': item['start_date'],
            'study_type': item['trial_type'] or 'N/A',  # TODO: review
            'study_design': item['trial_design'] or 'N/A',  # TODO: review
            'study_phase': item['trial_phase'] or 'N/A',  # TODO: review
            'primary_outcomes': None,  # TODO: review free text
            'secondary_outcomes': None,  # TODO: review free text
        }

        return trial

    def extract_problems(self, item):

        problems = []
        problems.append({
            'name': item['condition'],
            'type': 'condition',
        })

        return problems

    def extract_interventions(self, item):

        interventions = []

        for element in item['compound'] or []:

            interventions.append({
                'name': element,

            })

        return interventions

    def extract_locations(self, item):

        locations = []

        for element in item['locations'] or []:

            locations.append({
                'name': element,
                'type': 'country',
                'role': 'recruitment_countries',
            })

        return locations

    def extract_organisations(self, item):

        # TODO: review on scraper level
        organisations = []

        return organisations

    def extract_persons(self, item):

        # TODO: review on scraper level
        persons = []

        return persons
