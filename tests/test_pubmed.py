# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.pubmed.extractors import _find_identifiers


# Tests

def test_find_identifiers():
    text = 'Some NCT234134, NCT234 and UMIN23412 here!'
    result = _find_identifiers(text)
    assert result == ['NCT234134', 'NCT234', 'UMIN23412']
