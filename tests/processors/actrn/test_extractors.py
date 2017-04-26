# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import mock
import pytest
import processors.actrn.extractors as extractors


class TestActrnExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @pytest.mark.parametrize('age,expected_age_call', [
        ('12 Years', '12 Years'),
        (None, None),
    ])
    @mock.patch('processors.base.helpers.format_age', side_effect=lambda x: x)
    def test_extracts_minimum_and_maximum_ages(self, format_age_mock, stub_record, age, expected_age_call):
        stub_record.update({
            'minimum_age': age,
            'maximum_age': age,
        })

        trial = extractors.extract_trial(stub_record)

        assert trial['age_range'] == {
            'min_age': expected_age_call,
            'max_age': expected_age_call,
        }
        format_age_mock.assert_has_calls([
            mock.call(age),
            mock.call(age),
        ])



@pytest.fixture
def stub_record():
    return {
        'trial_id': 'NCT12345678',
        'public_title': 'Public title',
        'scientific_title': 'Public title',
        'brief_summary': 'Brief summary',
        'key_inclusion_criteria': 'Key inclusion criteria',
        'key_exclusion_criteria': 'Key exclusion criteria',
        'target_sample_size': 100,
        'anticipated_date_of_first_participant_enrolment': datetime.datetime(2017, 1, 1),
        'study_type': 'Interventional',
        'primary_outcomes': [],
        'secondary_outcomes': [],
        'gender': 'Both',
        'phase': 'Phase I',
        'date_registered': datetime.datetime(2017, 1, 1),
    }
