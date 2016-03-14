# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_persons():
    # persons/trials_persons

    for person in item['contacts'] or []:

        name = person.get('primary_contact', person.get('additional_contact'))
        if not name:
            continue

        person_id = upsert(db['persons'], ['name'], {
            'name': name,
            'type': None,
            'data': {},
        })

        upsert(db['trials_persons'], ['trial_id', 'person_id'], {
            'trial_id': trial_id,
            'person_id': person_id,
            'role': None,
            'context': person,
        }, auto_id=False)
