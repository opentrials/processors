# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.fixture
def fda_approval(conn, fda_application):
    fda_approval = {
        'id': ('%s-002' % fda_application),
        'supplement_number': 2,
        'type': 'Labeling',
        'action_date': '1990-08-07',
        'notes': 'Label is not available',
        'fda_application_id': fda_application,
    }
    fda_approval_id = conn['database']['fda_approvals'].insert(fda_approval)
    return fda_approval_id
