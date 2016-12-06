# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.fixture
def fda_application(conn, organization):
    fda_application = {
        'id': 'ANDA018659',
        'organisation_id': organization,
        'drug_name': 'ALLOPURINOL',
        'active_ingredients': 'ALLOPURINOL',
    }
    fda_application_id = conn['database']['fda_applications'].insert(fda_application)
    return fda_application_id
