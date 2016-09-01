# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.base import helpers


# Tests

def test_get_cleaned_identifiers():
    good_identifiers = {
        'actrn': 'ACTRN12615001075572p',
        'chictr': 'ChiCTR123',
        'drks': 'DRKS123',
        'euctr': 'EUCTR1234-123456-12',
        'gsk': 'GSK123',
        'irct': 'IRCT123',
        'isrctn': 'ISRCTN71203361',
        'jprn': 'JPRN-UMIN123456789',
        'kct': 'KCT123',
        'nct': 'NCT12345678',
        'ntr': 'NTR123',
        'pactr': 'PACTR123',
        'per': 'PER123',
        'rbr': 'RBR123',
        'rpcec': 'RPCEC123',
        'takeda': 'TAKEDA123',
        'tctr': 'TCTR123',
        'who': 'U1111-1115-2414',
    }
    bad_identifiers = {
        'bad_source': 'U123',
        'nct': 'ACTRN123',
        'actrn': '123ACTRN',
        'takeda': False,
        'jprn': None,
        'isrctn': 'ISRCTN12345678, ISRCTN12345678',
    }
    assert helpers.get_cleaned_identifiers(good_identifiers) == good_identifiers
    assert helpers.get_cleaned_identifiers(bad_identifiers) == {}


def test_find_list_of_identifiers():
    text = 'Some EUCTR2010-15, NCT234134, NCT234 and umin23412 here!'
    actual = helpers.find_list_of_identifiers(text)
    expect = [
        {'euctr': 'EUCTR2010-15'},
        {'jprn': 'umin23412'},
        {'nct': 'NCT234134'},
        {'nct': 'NCT234'}]
    assert actual ==  expect
