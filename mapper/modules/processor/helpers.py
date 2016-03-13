# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
from datetime import datetime


def update_trial(conn, mapping, identifier):

    # Get trial
    trial = None
    for key, value in mapping.items():
        if not value:
            continue
        trial = conn['trials'].find_one(**{key: value})
        if trial is not None:
            break

    # Prepare trial
    if trial is None:
        trial = dict(mapping)
        trial['uuid'] = uuid.uuid4().hex
        trial['records'] = []
    trial['updated'] = datetime.now()  # TODO: fix timezone
    if identifier not in trial['records']:
        trial['records'].append(identifier)

    # Save to backend
    conn['trials'].upsert(trial, ['uuid'], ensure=False)
