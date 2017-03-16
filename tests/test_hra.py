# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from processors.hra.extractors import _clean_identifier
from processors.hra.extractors import _url_from_title


# Tests

def test_clean_identifier():
    assert _clean_identifier('NCT12345678', prefix='NCT') == 'NCT12345678'
    assert _clean_identifier('12345678', prefix='NCT') == 'NCT12345678'
    assert _clean_identifier('ISRCTN12345678', prefix='ISRCTN') == 'ISRCTN12345678'
    assert _clean_identifier('12345678', prefix='ISRCTN') == 'ISRCTN12345678'
    assert _clean_identifier('n/a', prefix='NCT') is None


def test_url_from_title():
    title = 'Longterm F/U study of BOTOX® in Idiopathic Overactive Bladder patients'
    expected_url = 'http://www.hra.nhs.uk/news/research-summaries/longterm-fu-study-of-botox-in-idiopathic-overactive-bladder-patients'
    assert _url_from_title(title) == expected_url
