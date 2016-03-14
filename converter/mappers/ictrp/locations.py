# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_locations():
    # locations/trials_locations

    for location in item['location_countries'] or []:

        location_id = helpers.upsert(db['locations'], ['name', 'type'], {
            'name': location,
            'type': 'country',
            'data': {},
        })

        helpers.upsert(db['trials_locations'], ['trial_id', 'location_id'], {
            'trial_id': trial_id,
            'location_id': location_id,
            'role': 'recruitment_countries',
            'context': {},
        }, auto_id=False)
