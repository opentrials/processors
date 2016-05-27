# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base.readers.object import _make_array, _make_query


# Tests

def test_make_array():
    actual = _make_array(['el1', 'el2'])
    expect = "ARRAY['el1', 'el2']::text[]"
    assert actual == expect


def test_make_query():
    actual = _make_query('table', slug=None, facts=['fact1', 'fact2'])
    expect = "SELECT * from table WHERE facts && ARRAY['fact1', 'fact2']::text[]"
    assert actual == expect
