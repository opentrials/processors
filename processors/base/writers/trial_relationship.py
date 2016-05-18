# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def write_trial_relationship(conn, entity, relathionship):
    """Write trial relathionship to database.
    """
    table = 'trials_{entity}s'.format(entity=entity)
    keys = ['trial_id', '{entity}_id'.format(entity=entity)]
    conn['database'][table].upsert(relathionship, keys, ensure=False)
