# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import datetime
import pytest
import processors.nct.extractors as extractors


class TestNCTExtractors(object):
    STUB_RECORD = {
        'nct_id': 'NCT12345678',
        'brief_title': 'Public title',
        'official_title': 'Scientific title',
        'clinical_results': False,
        'firstreceived_date': datetime.date(2016, 1, 1),
        'brief_summary': 'Brief summary',
        'detailed_description': 'Detailed description',
        'eligibility': None,
        'start_date': datetime.date(2016, 1, 1),
        'study_type': 'Study type',
        'study_design': 'Study design',
        'phase': 'Phase',
        'primary_outcomes': 'Primary outcomes',
        'secondary_outcomes': 'Secondary outcomes',
        'secondary_ids': ['ISRCTN71203361'],
    }

    def test_stub_record_is_valid(self):
        record = copy.deepcopy(self.STUB_RECORD)
        extractors.extract_trial(record)

    @pytest.mark.parametrize('anticipated,actual,result', [
        (500, 200, 500),
        (0, 200, 0),
        (None, 500, 500),
        (None, None, None),
    ])
    def test_target_sample_size(self, anticipated, actual, result):
        record = copy.deepcopy(self.STUB_RECORD)
        record.update({
            'enrollment_anticipated': anticipated,
            'enrollment_actual': actual,
        })
        trial = extractors.extract_trial(record)

        assert trial['target_sample_size'] == result

    def test_extracted_identifiers(self):
        record = copy.deepcopy(self.STUB_RECORD)
        extracted_trial = extractors.extract_trial(record)

        expected_identifiers = {'nct': 'NCT12345678', 'isrctn': 'ISRCTN71203361'}
        assert extracted_trial['identifiers'] == expected_identifiers
