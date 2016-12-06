# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid


@pytest.fixture
def organization(conn, fda_source):
    organisation = {
        'id': uuid.uuid1().hex,
        'name': 'MYLAN',
        'source_id': fda_source,
        'slug': 'mylan',
    }
    organisation_id = conn['database']['organisations'].insert(organisation)
    return organisation_id
