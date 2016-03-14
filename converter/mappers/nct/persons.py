# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_persons():
    for person in item['overall_officials'] or []:

        # TODO: get more information
        if person.get('role', None) != 'Principal Investigator':
            continue

        person_id = helpers.upsert(db['persons'], ['name'], {
            'name': person['last_name'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trials_persons'], ['trial_id', 'person_id'], {
            'trial_id': trial_id,
            'person_id': person_id,
            'role': 'principal_investigator',
            'context': {},
        }, auto_id=False)
