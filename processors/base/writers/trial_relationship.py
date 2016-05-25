# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def write_trial_relationship(conn, entity_name, entity_data, entity_id, trial_id):
    """Write trial relathionship to database.
    """
    data = {}
    entity_id_field = '%s_id' % entity_name
    table = 'trials_%ss' % entity_name
    keys = ['trial_id', entity_id_field]
    data = {
        'trial_id': trial_id,
        entity_id_field: entity_id,
    }
    if entity in ['intervention', 'location', 'condition', 'person']:
        data.update({
            'role': entity_data['trial_role'],
        })
    conn['database'][table].upsert(data, keys, ensure=False)
