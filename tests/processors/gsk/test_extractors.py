# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import mock
import pytest
import processors.gsk.extractors as extractors


class TestGskExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @mock.patch('processors.base.helpers.format_age', side_effect=lambda x: x)
    def test_extracts_minimum_and_maximum_ages(self, format_age_mock, stub_record):
        age = 'age'
        stub_record.update({
            'minimum_age': age,
            'maximum_age': age,
        })

        trial = extractors.extract_trial(stub_record)

        assert trial['age_range'] == {
            'min_age': age,
            'max_age': age,
        }
        format_age_mock.assert_has_calls([
            mock.call(age),
            mock.call(age),
        ])


@pytest.fixture
def stub_record():
    return {
        'clinicaltrials_gov_identifier': 'NCT12345678',
        'study_id': 'GSK12345678',
        'study_title': 'Study title',
        'official_study_title': 'Official study title',
        'protocol_id': None,
        'brief_summary': 'Brief summary',
        'detailed_description': 'Detailed description',
        'eligibility_criteria': 'Criteria',
        'enrollment': 100,
        'study_start_date': datetime.datetime(2017, 1, 1),
        'study_type': 'Interventional',
        'study_design': 'Study design',
        'primary_outcomes': [],
        'secondary_outcomes': [],
        'gender': 'Both',
        'phase': 'Phase I',
        'first_received': datetime.datetime(2017, 1, 1),
        'record_verification_date': datetime.datetime(2017, 1, 1),
    }
