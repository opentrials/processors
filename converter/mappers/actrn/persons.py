# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_persons():
    # persons/trials_persons

    # TODO: process item['principal_investigator']

    person_id = upsert(db['persons'], ['name'], {
        'name': item['public_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'public_queries',
        'context': item['public_queries'],
    }, auto_id=False)

    person_id = upsert(db['persons'], ['name'], {
        'name': item['scientific_queries']['name'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_persons'], ['trial_id', 'person_id'], {
        'trial_id': trial_id,
        'person_id': person_id,
        'role': 'scientific_queries',
        'context': item['scientific_queries'],
    }, auto_id=False)
