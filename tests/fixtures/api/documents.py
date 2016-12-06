# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import pytest

@pytest.fixture
def fda_document(conn, fda_approval, fda_file, fda_source):
    document = {
        'id': uuid.uuid1().hex,
        'source_id': fda_source,
        'name': 'Printed Labeling',
        'type': 'other',
        'fda_approval_id': fda_approval,
        'file_id': fda_file,
        'source_url': None,
    }
    document_id = conn['database']['documents'].insert(document)
    return document_id
