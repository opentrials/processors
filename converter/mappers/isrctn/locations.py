# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_locations():
    # locations/trials_locations

    # TODO: move to scraper
    countries = (item['countries_of_recruitment'] or '').split(',') or []

    for country in countries:

        location_id = upsert(db['locations'], ['name', 'type'], {
            'name': country,
            'type': 'country',
            'data': {},
        })

        upsert(db['trials_locations'], ['trial_id', 'location_id'], {
            'trial_id': trial_id,
            'location_id': location_id,
            'role': 'recruitment_countries',
            'context': {},
        }, auto_id=False)
