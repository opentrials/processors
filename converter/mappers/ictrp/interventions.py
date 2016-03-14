# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_interventions():
    for intervention in item['interventions'] or []:

        intervention_id = helpers.upsert(db['interventions'], ['name', 'type'], {
            'name': intervention['intervention_name'],
            'type': None,
            'data': {},
        })

        helpers.upsert(db['trials_interventions'], ['trial_id', 'intervention_id'], {
            'trial_id': trial_id,
            'intervention_id': intervention_id,
            'role': None,
            'context': intervention,
        }, auto_id=False)
