# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_organisations():
    for sponsor in item['sponsors'] or []:

        # TODO: get more information
        sponsor = sponsor.get('lead_sponsor', None)
        if sponsor is None:
            continue

        organisation_id = helpers.upsert(db['organisations'], ['name'], {
            'name': sponsor['agency'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'primary_sponsor',
            'context': {},
        }, auto_id=False)
