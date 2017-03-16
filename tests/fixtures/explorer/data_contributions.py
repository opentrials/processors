# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid

@pytest.fixture
def data_contribution(conn, trial, document_category):
    data_contribution = {
        'id': uuid.uuid1().hex,
        'user_id': None,
        'trial_id': trial,
        'data_url': None,
        'comments': None,
        'approved': True,
        'curation_comments': None,
        'url': 'http://www.example.com',
        'document_category_id': document_category,
        'document_id': None,
    }
    contrib_id = conn['explorer']['data_contributions'].insert(data_contribution)
    return contrib_id
