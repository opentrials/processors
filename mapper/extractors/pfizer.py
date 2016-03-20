# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class PfizerExtractor(base.Extractor):

    # Public

    direct = True
    table = 'data_pfizer'

    def extract_source(self):

        source = {
            'name': 'pfizer',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'nct_id': item['nct_id'],
            'primary_register': 'pfizer',
            'primary_id': item['nct_id'],
            'secondary_ids': {'nct_id': item['nct_id'] },
            'registration_date': item['study_start_date'],  # TODO: review
            'public_title': item['title'],  # TODO: review
            'brief_summary': '',  # TODO: review
            'scientific_title': None,  # TODO: review
            'description': None,  # TODO: review
            'recruitment_status': item['status'],
            'eligibility_criteria': {'criteria': item['overall_status']},
            'target_sample_size': None,
            'first_enrollment_date': item['study_start_date'],
            'study_type': item['study_type'],
            'study_design': None,  # TODO: review
            'study_phase': None,  # TODO: review
            'primary_outcomes': None,  # TODO: review
            'secondary_outcomes': None,  # TODO: review
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
                'nct_id': item['nct_id'],
            },
        }

        return record

    def extract_problems(self, item):

        # TODO: check on scraper level
        problems = []

        return problems

    def extract_interventions(self, item):

        # TODO: check on scraper level
        interventions = []

        return interventions

    def extract_locations(self, item):

        # TODO: check on scraper level
        locations = []

        return locations

    def extract_organisations(self, item):

        # TODO: check on scraper level
        organisations = []

        return organisations

    def extract_persons(self, item):

        # TODO: check on scraper level
        persons = []

        return persons
