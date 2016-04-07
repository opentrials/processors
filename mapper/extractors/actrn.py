# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


# Module API

class ActrnExtractor(base.Extractor):

    # Public

    store = 'warehouse'
    table = 'actrn'
    heads = ['nct', 'euctr', 'isrctn']

    def extract_source(self, item):

        source = {
            'name': 'actrn',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
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
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {
                'inclusion': item['key_inclusion_criteria'],
                'exclusion': item['key_exclusion_criteria'],
            },
            'target_sample_size': item['target_sample_size'],
            'first_enrollment_date': item['anticipated_date_of_first_participant_enrolment'],  # TODO: review
            'study_type': item['study_type'],
            'study_design': 'N/A',  # TODO: review
            'study_phase': item['phase'] or 'N/A',  # TODO: review
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['secondary_outcomes'] or [],
        }

        return trial

    def extract_problems(self, item):

        # TODO: item['health_conditions_or_problems_studied'] - free text some time
        problems = []

        return problems

    def extract_interventions(self, item):

        # TODO: item['intervention_codes'] - discover
        interventions = []

        return interventions

    def extract_locations(self, item):

        # TODO: no recruitment countries
        locations = []

        return locations

    def extract_organisations(self, item):

        organisations = []

        for element in item['sponsors'] or []:

            # TODO: process item['primary_sponsor']
            if 'name' not in element:
                continue

            organisations.append({
                'name': element['name'],
                'role': 'sponsor',  # TODO: review
                'context': element,
            })

        return organisations

    def extract_persons(self, item):

        persons = []

        # TODO: process item['principal_investigator']
        for role in ['public_queries', 'scientific_queries']:

            persons.append({
                'name': item[role]['name'],
                'role': role,
                'context': item[role],
            })

        return persons
