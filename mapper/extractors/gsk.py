# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class GskExtractor(base.Extractor):

    # Public

    basis = 'warehouse'
    table = 'data_gsk'

    def extract_source(self, item):

        source = {
            'name': 'gsk',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'nct_id': item['clinicaltrialsgov_identifier'],
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
            'recruitment_status': item['study_recruitment_status'],
            'eligibility_criteria': {
                'criteria': item['eligibility_criteria'],  # TODO: bad text - fix on scraper
            },
            'target_sample_size': item['enrollment'],  # TODO: review
            'first_enrollment_date': item['study_start_date'],
            'study_type': item['study_type'],  # TODO: review
            'study_design': item['study_design'] or 'N/A',  # TODO: review
            'study_phase': item['phase'] or 'N/A',  # TODO: review
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['secondary_outcomes'] or [],
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
                'study_id': item['study_id'],
            },
        }

        return record

    def extract_problems(self, item):

        problems = []

        for element in item['conditions'] or []:

            problems.append({
                'name': element,
            })

        return problems

    def extract_interventions(self, item):

        # TODO: item['interventions'] - reimplement on scraper - array -> dict
        interventsion = []

        return interventions

    def extract_locations(self, item):

        # TODO: no recruitment countries field
        locations = []

        return locations

    def extract_organisations(self, item):

        # TODO: discover how to get it/fix it on scraper
        organisations = []

        return organisations

    def extract_persons(self, item):

        # TODO: discover how to get it/fix it on scraper
        persons = []

        return persons
