# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import pytest

@pytest.fixture
def fda_document(conn, fda_approval, fda_file, fda_source, document_category):
    document = {
        'id': uuid.uuid1().hex,
        'source_id': fda_source,
        'name': 'Printed Labeling',
        'fda_approval_id': fda_approval,
        'file_id': fda_file,
        'source_url': None,
        'document_category_id': document_category,
    }
    document_id = conn['database']['documents'].insert(document)
    return document_id

@pytest.fixture
def document(conn, file_fixture, nct_source, document_category):
    document = {
        'id': uuid.uuid1().hex,
        'source_id': nct_source,
        'name': 'Printed Labeling',
        'fda_approval_id': None,
        'file_id': file_fixture,
        'source_url': None,
        'document_category_id': document_category,
    }
    document_id = conn['database']['documents'].insert(document)
    return document_id
