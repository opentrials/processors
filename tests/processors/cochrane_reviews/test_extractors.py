# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import processors.cochrane_reviews.extractors as extractors


class TestCochraneExtractors(object):
    def test_extract_review_results(self):
        results = [
            {'result': 'UNKNOWN', 'rob_name': 'Random sequence generation (selection bias)'},
            {'result': 'NO', 'rob_name': 'Allocation concealment (selection bias)'},
            {'result': 'YES', 'rob_name': 'Detection bias'},
            {'result': 'YES', 'rob_name': 'Incomplete outcome data'},
            {'result': 'YES', 'rob_name': 'Reporting bias'},
            {'result': 'NO', 'rob_name': 'Free of other bias'}
        ]
        processed_results = extractors.extract_review_results(results)
        expected = [{'name':'sequence generation', 'value':'unknown'},
                    {'name':'allocation concealment', 'value':'no'},
                    {'name':'blinding (detection)', 'value':'yes'},
                    {'name':'attrition', 'value':'yes'},
                    {'name':'other biases', 'value':'no'}]
        assert processed_results == expected
