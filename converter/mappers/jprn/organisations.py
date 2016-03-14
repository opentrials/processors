# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_organisations():
    # organisations/trials_organisations

    organisation_id = upsert(db['organisations'], ['name'], {
        'name': item['name_of_primary_sponsor'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
        'trial_id': trial_id,
        'organisation_id': organisation_id,
        'role': 'primary_sponsor',
        'context': {},
    }, auto_id=False)

    organisation_id = upsert(db['organisations'], ['name'], {
        'name': item['source_of_funding'],
        'type': None,
        'data': {},
    })

    upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
        'trial_id': trial_id,
        'organisation_id': organisation_id,
        'role': 'funder',
        'context': {},
    }, auto_id=False)
