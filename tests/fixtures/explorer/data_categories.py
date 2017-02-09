# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import random

@pytest.fixture
def data_category(conn):
    data_category = {
        'id': random.randint(0,1000),
        'name': 'Journal article',
        'group': 'Results',
    }
    category_id = conn['explorer']['data_categories'].insert(data_category)
    return category_id
