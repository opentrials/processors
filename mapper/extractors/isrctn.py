# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import base
logger = logging.getLogger(__name__)


class IsrctnExtractor(base.Extractor):

    # Public

    direct = True
    table = 'isrctn'

    def extract_source(self, item):

        source = {
            'name': 'isrctn',
            'type': 'register',
        }

        return source

    def extract_trial(self, item):

        # TODO: review
        try:
            target_sample_size = int(item['target_number_of_participants'])
        except Exception:
            target_sample_size = None

        trial = {
            'nct_id': item['clinicaltrialsgov_number'],
            'isrctn_id': item['isrctn_id'],
            'primary_register': 'isrctn',
            'primary_id': item['isrctn_id'],
            'secondary_ids': {
                'doi_isrctn': item['doi_isrctn_id'],  # TODO: remove isrct part
                'euctr': item['eudract_number'],
                'nct': item['clinicaltrialsgov_number'],
            },
            'registration_date': item['date_applied'],  # TODO: review
            'public_title': item['title'],
            'brief_summary': item['plain_english_summary'],
            'scientific_title': item['scientific_title'],
            'description': None,  # TODO: review
            'recruitment_status': item['recruitment_status'],
            'eligibility_criteria': {
                'inclusion': item['participant_inclusion_criteria'],
                'exclusion': item['participant_exclusion_criteria'],
            },
            'target_sample_size': target_sample_size,
            'first_enrollment_date': item['overall_trial_start_date'],
            'study_type': item['primary_study_design'],
            'study_design': item['study_design'],
            'study_phase': item['phase'] or 'N/A',  # TODO: review
            'primary_outcomes': item['primary_outcome_measures'] or [],
            'secondary_outcomes': item['secondary_outcome_measures'] or [],
        }

        return trial

    def extract_record(self, item):

        record = {
            'type': 'trial',
            'data': {
                # TODO: item seriliazation issue
                'isrctn_id': item['isrctn_id'],
            },
        }

        return record

    def extract_problems(self, item):

        # TODO: item['condition'] - free text
        problems = []

        return problems

    def extract_interventions(self, item):

        # TODO: item['interventions'] - free text
        # TODO: item['drug_names'] - free text
        interventions = []

        return interventions

    def extract_locations(self, item):

        locations = []

        # TODO: move split to scraper
        for element in (item['countries_of_recruitment'] or '').split(',') or []:  # noqa

            locations.append({
                'name': element,
                'type': 'coutnry',
                'role': 'recruitment_countries',
            })

        return locations

    def extract_organisations(self, item):

        organisations = []

        for element in item['sponsors'] or []:

            organisations.append({
                'name': element['organisation'],
                'data': element,
                'role': 'sponsor',
            })

        for element in item['funders'] or []:

            organisations.append({
                'name': element['funder_name'],
                'data': element,
                'role': 'funder',
            })

        return organisations

    def extract_persons(self, item):

        persons = []

        for element in item['contacts'] or []:

            # TODO: review
            name = element.get('primary_contact', element.get('additional_contact'))
            if not name:
                continue

            persons.append({
                'name': name,
                'context': element
            })

        return persons
