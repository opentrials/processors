# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'hra',
        'name': 'Health Research Authority',
        'type': 'other',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': _clean_identifier(record['nct_id'], prefix='NCT'),
        'isrctn': _clean_identifier(record['isrctn_id'], prefix='ISRCTN'),
        'hra': record['hra_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['application_title'],
        record['application_full_title'],
        record['hra_id'])

    # Compose trial
    trial = {
        'primary_register': 'Health Research Authority',
        'primary_id': record['hra_id'],
        'identifiers': identifiers,
        'registration_date': record['publication_date'],
        'public_title': public_title,
        'brief_summary': record['research_summary'],
        'scientific_title': record['application_full_title'],
        'study_type': record['study_type'],
    }

    return trial


def extract_conditions(record):
    conditions = []
    return conditions


def extract_interventions(record):
    interventions = []
    return interventions


def extract_locations(record):
    locations = []
    return locations


def extract_organisations(record):
    organisations = []
    organisations.append({
        'name': record['sponsor_org'],
        'role': 'primary_sponsor',
    })
    organisations.append({
        'name': record['establishment_org'],
    })
    return organisations


def extract_persons(record):
    persons = []
    persons.append({
        'name': record['contact_name'],
        # ---
        'trial_id': record['hra_id'],
        'trial_role': 'public_queries',
    })
    return persons


# Internal

def _clean_identifier(ident, prefix):
    if re.match(r'%s\d{3,}' % prefix, ident):
        return ident
    if re.match(r'\d{3,}', ident):
        return '%s%s' % (prefix, ident)
    return None
