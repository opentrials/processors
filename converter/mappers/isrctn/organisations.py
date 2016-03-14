# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_organisations():
    # organisations/trials_organisations

    for sponsor in item['sponsors'] or []:

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': sponsor['organisation'],
            'type': None,
            'data': sponsor,
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'sponsor',
            'context': {},
        }, auto_id=False)

    for funder in item['funders'] or []:

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': funder['funder_name'],
            'type': None,
            'data': funder,
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'funder',
            'context': {},
        }, auto_id=False)
