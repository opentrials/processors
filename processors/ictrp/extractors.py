# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import logging
from datetime import datetime
from .. import base

logger = logging.getLogger(__name__)


# Module API

def extract_source(record):
    source = {
        'id': 'ictrp',
        'name': 'WHO ICTRP',
        'type': 'register',
        'source_url': 'http://www.who.int/trialsearch/',
        'terms_and_conditions_url': 'http://www.who.int/ictrp/search/download/en/',
    }
    return source


def extract_trial(record):

    # Get identifiers
    registries = {
        'ANZCTR': 'actrn',  # Australia
        'ChiCTR': 'chictr',  # China
        'ClinicalTrials.gov': 'nct',
        'EUCTR': 'euctr',
        'German Clinical Trials Register': 'drks',  # German
        'IRCT': 'irct',  # Iran
        'ISRCTN': 'isrctn',
        'JPRN': 'jprn',  # Japan
        'KCT': 'kct',  # Korea
        'Netherlands Trial Register': 'ntr',  # Netherlands
        'PACTR': 'pactr',  # Pan Africa
        'REBEC': 'rbr',  # Brazil
        'RPCEC': 'rpcec',  # Cuba
        'RPEC': 'per',  # Peru
        'TCTR': 'tctr',  # Thai
    }
    source_id = registries[record['register']]
    identifier = record['main_id']
    # Extract EUCTR master identifier
    if source_id == 'euctr' and len(identifier) > 19:
        identifier = identifier.rsplit('-', 1)[0]
    identifiers = base.helpers.clean_identifiers({
        source_id: identifier,
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['public_title'],
        record['scientific_title'],
        record['main_id'],
    )

    # Get status and recruitment status
    statuses = {
        '': [None, None],
        'active, not recruiting': ['ongoing', 'not_recruiting'],
        'active': ['ongoing', 'unknown'],
        'approved for marketing': ['other', 'other'],
        'authorised-recruitment may be ongoing or finished': ['ongoing', 'unknown'],
        'available': ['ongoing', 'unknown'],
        'canceled': ['terminated', 'not_recruiting'],
        'closed: follow-up complete': ['complete', 'not_recruiting'],
        'closed: follow-up continuing': ['ongoing', 'not_recruiting'],
        'closed to recruitment: follow up complete': ['complete', 'not_recruiting'],
        'closed to recruitment: follow up continuing': ['ongoing', 'not_recruiting'],
        'complete': ['complete', 'not_recruiting'],
        'completed': ['complete', 'not_recruiting'],
        'completed: recruitment & data analysis complete': ['complete', 'not_recruiting'],
        'complete: follow-up complete': ['complete', 'not_recruiting'],
        'complete: follow-up continuing': ['ongoing', 'not_recruiting'],
        'data analysis completed': ['complete', 'not_recruiting'],
        'early termination': ['terminated', 'not_recruiting'],
        'enrolling by invitation': ['ongoing', 'recruiting'],
        'finished': ['complete', 'not_recruiting'],
        'interrupted': ['suspended', 'not_recruiting'],
        'main results already published': ['complete', 'not_recruiting'],
        'no longer available': ['other', 'other'],
        'no longer recruiting': ['ongoing', 'not_recruiting'],
        'non authorized': ['other', 'other'],
        'not recruiting': ['ongoing', 'not_recruiting'],
        'not yet recruiting': ['ongoing', 'not_recruiting'],
        'open public recruiting': ['ongoing', 'recruiting'],
        'open to recruitment: actively recruiting participa': ['ongoing', 'recruiting'],
        'other': ['other', 'other'],
        'pending (not yet recruiting)': ['ongoing', 'not_recruiting'],
        'pending': ['ongoing', 'unknown'],
        'recruiting': ['ongoing', 'recruiting'],
        'recruitment completed': ['ongoing', 'not_recruiting'],
        'stopped early': ['terminated', 'not_recruiting'],
        'suspended': ['suspended', 'not_recruiting'],
        'temporarily closed': ['suspended', 'not_recruiting'],
        'temporarily not available': ['other', 'other'],
        'temporary halt or suspension': ['suspended', 'not_recruiting'],
        'temporary halt': ['suspended', 'not_recruiting'],
        'terminated': ['terminated', 'not_recruiting'],
        'withdrawn': ['withdrawn', 'not_recruiting'],
        'withheld': ['other', 'other'],
    }
    key = record.get('recruitment_status', '').strip().lower()
    status, recruitment_status = statuses[key]

    # Get gender
    gender = None

    # Get has_published_results
    has_published_results = None

    # Registration date
    registration_date = None
    date_of_registration = record.get('date_of_registration')
    if date_of_registration:
        date_formats = [
            '%d/%m/%Y',
            '%Y-%m-%d',
        ]
        for fmt in date_formats:
            try:
                registration_date = datetime.strptime(date_of_registration, fmt).date()
                break
            except ValueError:
                pass
        if not registration_date:
            logger.warn("Failed to parse date '%s'" % date_of_registration)

    trial = {
        'identifiers': identifiers,
        'public_title': public_title,
        'scientific_title': record['scientific_title'],
        'status': status,
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['key_inclusion_exclusion_criteria']},
        'target_sample_size': record['target_sample_size'],
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': record['study_phase'],
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
        'registration_date': registration_date,
    }
    return trial


def extract_conditions(record):
    conditions = []
    for element in record['health_conditions_or_problems_studied'] or []:
        conditions.append({
            'name': element,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    pattern = r'(?:Intervention\s*)?\d[.):]'
    for element in record['interventions'] or []:
        for name in re.split(pattern, element):
            interventions.append({
                'name': name,
            })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['countries_of_recruitment'] or []:
        for index, name in enumerate(re.split(r'[,;]', element)):
            name = name.strip()
            # For cases like "Venezuela, Bolivarian Republic of"
            if index == 1 and 'republic of' in name.lower():
                continue
            locations.append({
                'name': name,
                'type': 'country',
                # ---
                'trial_role': 'recruitment_countries',
            })
    return locations


def extract_organisations(record):
    organisations = []
    return organisations


def extract_persons(record):
    persons = []
    return persons
