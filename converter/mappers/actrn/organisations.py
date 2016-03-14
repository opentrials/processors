# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_organisations():
    # organisations/trials_organisations

    for sponsor in item['sponsors'] or []:

        # TODO: process item['primary_sponsor']

        if 'name' not in sponsor:
            continue

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': sponsor['name'],
            'type': None,
            'data': sponsor,
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'sponsor',  # TODO: review
            'context': {},
        }, auto_id=False)
