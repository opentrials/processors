# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base import helpers


# Tests

def test_find_list_of_identifiers():
    text = 'Some EUCTR2010-15, NCT234134, NCT234 and umin23412 here!'
    actual = helpers.find_list_of_identifiers(text)
    expect = [
        {'euctr': 'EUCTR2010-15'},
        {'jprn': 'umin23412'},
        {'nct': 'NCT234134'},
        {'nct': 'NCT234'}]
    assert actual ==  expect
