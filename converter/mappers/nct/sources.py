# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ... import indexers
from .. import helpers


def map_sources(source, target):

    id = indexers.index_source(source,
        name='nct',
        type='register',
    )

    helpers.upsert(target['sources'], {
        'id': id,
        'name': 'nct',
        'type': 'register',
        'data': {},
    })

    return id
