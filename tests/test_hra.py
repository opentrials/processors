# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.hra.extractors import _clean_identifier


# Tests

def test_clean_identifier():
    assert _clean_identifier('NCT12345678', prefix='NCT') == 'NCT12345678'
    assert _clean_identifier('12345678', prefix='NCT') == 'NCT12345678'
    assert _clean_identifier('ISRCTN12345678', prefix='ISRCTN') == 'ISRCTN12345678'
    assert _clean_identifier('12345678', prefix='ISRCTN') == 'ISRCTN12345678'
    assert _clean_identifier('n/a', prefix='NCT') == None
