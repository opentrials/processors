# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def map_item_problems():

    # problems/trials_problems

    for condition in item['conditions'] or []:

        problem_id = upsert(db['problems'], ['name', 'type'], {
            'name': condition,
            'type': None,
            'data': {},
        })

        upsert(db['trials_problems'], ['trial_id', 'problem_id'], {
            'trial_id': trial_id,
            'problem_id': problem_id,
            'role': None,
            'context': {},
        }, auto_id=False)
