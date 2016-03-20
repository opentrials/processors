# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class NctExtractor(base.Extractor):

    # Public

    basis = 'warehouse'
    table = 'data_nct'

    def extract_source(self, item):

        source = {
            'name': 'nct',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'nct_id': item['nct_id'],
            'primary_register': 'nct',
            'primary_id': item['nct_id'],
            'secondary_ids': {'others': item['secondary_ids'] },
            'registration_date': item['firstreceived_date'],
            'public_title': item['brief_title'],
            'brief_summary': item['brief_summary'] or '',  # TODO: review
            'scientific_title': item['official_title'],
            'description': item['detailed_description'],
            'recruitment_status': item['overall_status'],
            'eligibility_criteria': item['eligibility'],
            'target_sample_size': item['enrollment_anticipated'],
            'first_enrollment_date': item['start_date'],
            'study_type': item['study_type'],
            'study_design': item['study_design'],
            'study_phase': item['phase'],
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['secondary_outcomes'] or [],
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

        problems = []

        for element in item['conditions'] or []:

            problems.append({
                'name': element,
            })

        return problems

    def extract_interventions(self, item):

        interventions = []

        for element in item['interventions'] or []:

            interventsion.append({
                'name': element['intervention_name'],
                'context': element,
            })

        return interventions

    def extract_locations(self, item):

        locations = []

        for element in item['location_countries'] or []:

            locations.append({
                'name': element,
                'type': 'country',
                'role': 'recruitment_countries',
            })

        return locations

    def extract_organisations(self, item):

        organisations = []

        for element in item['sponsors'] or []:

            # TODO: get more information
            element = element.get('lead_sponsor', None)
            if element is None:
                continue

            organisations.append({
                'name': element['agency'],
                'role': 'primary_sponsor',
            })

        return organisations

    def extract_persons(self, item):

        persons = []

        for element in item['overall_officials'] or []:

            # TODO: get more information
            if element.get('role', None) != 'Principal Investigator':
                continue

            persons.append({
                'name': element['last_name'],
                'role': 'principal_investigator',
            })

        return persons
