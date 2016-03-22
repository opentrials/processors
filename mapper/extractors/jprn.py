# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


# Module API

class JprnExtractor(base.Extractor):

    # Public

    store = 'warehouse'
    table = 'data_jprn'

    def extract_source(self, item):

        source = {
            'name': 'jprn',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        trial = {
            'primary_register': 'jprn',
            'primary_id': item['unique_trial_number'],
            'secondary_ids': {},  # TODO: use item['secondary_study_id_*'] and item['org_issuing_secondary_study_id_*']
            'registration_date': item['date_of_registration'],
            'public_title': item['title_of_the_study'],
            'brief_summary': 'N/A',  # TODO: review
            'scientific_title': item['official_scientific_title_of_the_study'],
            'description': None,  # TODO: review
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {
                'inclusion': item['key_inclusion_criteria'],
                'exclusion': item['key_exclusion_criteria'],
            },
            'target_sample_size': item['target_sample_size'],
            'first_enrollment_date': item['anticipated_trial_start_date'],  # TODO: review
            'study_type': item['study_type'] or 'N/A',  # TODO: review
            'study_design': item['basic_design'] or 'N/A',  # TODO: review
            'study_phase': item['developmental_phase'] or 'N/A',  # TODO: review
            'primary_outcomes': item['primary_outcomes'] or [],
            'secondary_outcomes': item['key_secondary_outcomes'] or [],
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
                'unique_trial_number': item['unique_trial_number'],
            },
        }

        return record

    def extract_problems(self, item):

        # TODO: item['condition'] - free text some time
        problems = []

        return problems

    def extract_interventions(self, item):

        # TODO: item['interventions'] - array of free texts
        interventions = []

        return interventions

    def extract_locations(self, item):

        # TODO: fix on scraper item['region'] when possible
        locations = []

        return locations

    def extract_organisations(self, item):

        organisations = []
        organisations.append({
            'name': item['name_of_primary_sponsor'],
            'role': 'primary_sponsor',
        })
        organisations.append({
            'name': item['source_of_funding'],
            'role': 'funder',
        })

        return organisations

    def extract_persons(self, item):

        persons = []
        if item['research_name_of_lead_principal_investigator']:
            persons.append({
                'name': item['research_name_of_lead_principal_investigator'],
                'role': 'principal_investigator',
                'context': {
                    'research_name_of_lead_principal_investigator': item['research_name_of_lead_principal_investigator'],
                    'research_organization': item['research_organization'],
                    'research_division_name': item['research_division_name'],
                    'research_address': item['research_address'],
                    'research_tel': item['research_tel'],
                    'research_homepage_url': item['research_homepage_url'],
                    'research_email': item['research_email'],
                },
            })
        if item['public_name_of_contact_person']:
            persons.append({
                'name': item['public_name_of_contact_person'],
                'role': 'public_queries',
                'context': {
                    'public_name_of_contact_person': item['public_name_of_contact_person'],
                    'public_organization': item['public_organization'],
                    'public_division_name': item['public_division_name'],
                    'public_address': item['public_address'],
                    'public_tel': item['public_tel'],
                    'public_homepage_url': item['public_homepage_url'],
                    'public_email': item['public_email'],
                },
            })

        return persons
