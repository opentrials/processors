# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'icdpcs',
        'name': 'ICD-PCS',
        'type': 'other',
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
        name = base.helpers.clean_string(name)
        if name:
            interventions.append({
                'name': name,
                'type': 'procedure',
                'icdpcs_code': record['code'],
            })

    return interventions
