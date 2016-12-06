# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import datetime
import pytest
import processors.ictrp.extractors as extractors


class TestICTRPExtractors(object):
    @pytest.mark.parametrize('date_str,expected_date', [
        ('2012-12-31', datetime.date(2012, 12, 31)),
        ('31/12/2012', datetime.date(2012, 12, 31)),
        ('2012-05-01', datetime.date(2012, 5, 1)),
        ('01/05/2012', datetime.date(2012, 5, 1)),
        ('invalid', None),
        ('', None),
    ])
    def test_extract_trial_handles_dates(self, date_str, expected_date, stub_record):
        stub_record['date_of_registration'] = date_str

        trial = extractors.extract_trial(stub_record)

        assert trial.get('registration_date') == expected_date


@pytest.fixture
def stub_record():
    return {
        'register': 'ClinicalTrials.gov',
        'main_id': 'NCT0000000',
        'public_title': 'Public title',
        'scientific_title': 'Scientific title',
        'target_sample_size': 100,
        'study_type': 'study_type',
        'study_design': 'study design',
        'study_phase': 'study phase',
        'primary_outcomes': 'primary outcomes',
        'secondary_outcomes': 'secondary outcomes',
        'key_inclusion_exclusion_criteria': 'key inclusion exclusion criteria',
    }
