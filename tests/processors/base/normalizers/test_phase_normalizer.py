# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from processors.base.normalizers import get_normalized_phase

#Tests
class TestValidateRemoteURL(object):
    @pytest.mark.parametrize('test_input,expected', [
            ('Phase 3 / Phase 4', ['Phase 3', 'Phase 4']),
            ('I-IIA', ['Phase 1', 'Phase 2A']),
            ('Human pharmacology (Phase I): yes\\nTherapeutic exploratory'+
                ' (Phase II): yes\\nTherapeutic confirmatory - (Phase III):'+
                ' no\\nTherapeutic use (Phase IV): no\\n', ['Phase 1', 'Phase 2']),
            ('Not applicable', ['Not applicable']),
            ('Not Specified', ['Not applicable']),
            ('N/A', ['Not applicable']),
            ('n\\a', ['Not applicable']),
            ('N/', ['Not applicable']),
            ('IIA', ['Phase 2A']),
            ('IIIB', ['Phase 3B']),
            ('0(exploratory trials))', ['Phase 0']),
            ('I (Phase I study)', ['Phase 1']),
            ('Post-market', ['Phase 4']),
            ('Pilot study', ['Other']),
            ('Diagnostic New Technique Clincal Study', ['Other']),
            (None, None),
            ('', None),
            ('()', ['()']),
            ('[]', ['[]']),
            # This test case is not in the json variations file
            ('Phase 1/2/3/4', ['Phase 1/2/3/4'])
        ])

    def test_phase_normalizer(self, test_input, expected):
        assert get_normalized_phase(test_input) == expected
