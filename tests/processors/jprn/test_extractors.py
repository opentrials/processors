# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import mock
import pytest
import processors.jprn.extractors as extractors


class TestJprnExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @pytest.mark.parametrize('age,expected_age_call', [
        ('12 years-old >=', '12 years'),
        ('1 months-old >', '1 months'),
        ('Some age', 'Some age'),
        (None, ''),
    ])
    @mock.patch('processors.base.helpers.format_age', side_effect=lambda x: x)
    def test_extracts_minimum_and_maximum_ages(self, format_age_mock, stub_record, age, expected_age_call):
        stub_record.update({
            'ageupper_limit': age,
            'agelower_limit': age,
        })

        trial = extractors.extract_trial(stub_record)

        assert trial['age_range'] == {
            'min_age': expected_age_call,
            'max_age': expected_age_call,
        }
        format_age_mock.assert_has_calls([
            mock.call(expected_age_call),
            mock.call(expected_age_call),
        ])



@pytest.fixture
def stub_record():
    return {
        'study_title': 'Study title',
        'title_of_the_study': 'Official study title',
        'official_scientific_title_of_the_study': 'Official study title',
        'unique_trial_number': '123456',
        'publication_of_results': 'Published',
        'narrative_objectives1': 'Brief summary',
        'key_inclusion_criteria': 'Criteria',
        'key_exclusion_criteria': 'Criteria',
        'target_sample_size': 100,
        'anticipated_trial_start_date': datetime.datetime(2017, 1, 1),
        'study_type': 'Interventional',
        'basic_design': 'Study design',
        'primary_outcomes': [],
        'key_secondary_outcomes': [],
        'gender': 'Male and Female',
        'developmental_phase': 'Phase I',
        'date_of_registration': datetime.datetime(2017, 1, 1),
        'ageupper_limit': '',
        'agelower_limit': '',
    }
