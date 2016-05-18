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


def extract_problems(record):

    # Get all names
    names = []
    names.append(record['desc'])
    names = names + record['terms']

    # Extract problems
    problems = []
    for name in names:
        problems.append({
            'name': name,
            'type': 'condition',
            'data': {},
            'role': None,
            'context': {},
            'description': None,
            'icdcm_code': record['name'],
        })

    return problems