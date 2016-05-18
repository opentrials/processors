# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'id': 'icdcm',
        'name': 'ICD-CM',
        'type': 'other',
        'data': {},
    }
    return source


def extract_conditions(record):

    # Get all names
    names = []
    names.append(record['desc'])
    names = names + record['terms']

    # Extract conditions
    conditions = []
    for name in names:
        conditions.append({
            'name': name,
            'data': {},
            'role': None,
            'context': {},
            'description': None,
            'icdcm_code': record['name'],
        })

    return conditions
