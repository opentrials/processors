# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'id': 'icdpcs',
        'name': 'ICD-10 Procedure Coding System',
        'type': 'other',
        'url': 'https://www.cms.gov/Medicare/Coding/ICD10/index.html',
    }
    return source


def extract_interventions(record):

    # Get all names
    names = []
    names.append(record['short_description'])
    names.append(record['long_description'])

    # Extract interventions
    interventions = []
    for name in names:
        interventions.append({
            'name': name,
            'type': 'procedure',
            'icdpcs_code': record['code'],
        })

    return interventions
