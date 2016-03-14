# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_organisations():
    # organisations/trials_organisations

    for sponsor in item['sponsors'] or []:

        if 'name_of_sponsor' not in intervention:
            continue

        organisation_id = upsert(db['organisations'], ['name'], {
            'name': sponsor['name_of_sponsor'],
            'type': None,
            'data': {},
        })

        upsert(db['trials_organisations'], ['trial_id', 'organisation_id'], {
            'trial_id': trial_id,
            'organisation_id': organisation_id,
            'role': 'sponsor',
            'context': sponsor,
        }, auto_id=False)
