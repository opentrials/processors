# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

@pytest.fixture
def document_category(conn):
    document_category = {
        'id': 1,
        'name': 'Result paper',
        'group': 'Results',
    }
    doc_category_id = conn['database']['document_categories'].insert(document_category)
    return doc_category_id
