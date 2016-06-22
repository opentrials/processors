# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base.helpers import find_identifiers


# Tests

def test_find_identifiers():
    text = 'Some EUCTR2010-15, NCT234134, NCT234 and umin23412 here!'
    result = find_identifiers(text)
    assert result == ['EUCTR2010-15', 'NCT234134', 'NCT234', 'umin23412']
