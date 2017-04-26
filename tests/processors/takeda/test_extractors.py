# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import mock
import pytest
import processors.takeda.extractors as extractors


class TestTakedaExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @pytest.mark.parametrize('age,expected_min_age,expected_max_age', [
        ('12 Years and up', '12 Years', 'any'),
        ('Up to 50 Years', 'any', '50 Years'),
        ('1 Year-1 Year', '1 Year', '1 Year'),
        ('N/A - N/A', 'N/A', 'N/A'),
        (None, None, None),
    ])
    def test_extracts_minimum_and_maximum_ages(self, stub_record, age, expected_min_age, expected_max_age):
        stub_record.update({
            'ages': age,
        })

        trial = extractors.extract_trial(stub_record)

        assert trial['age_range'] == {
            'min_age': expected_min_age,
            'max_age': expected_max_age,
        }


@pytest.fixture
def stub_record():
    return {
        'nct_number': 'NCT12345678',
        'takeda_trial_id': '12345678',
        'official_title': 'Scientific title',
        'gender': 'both',
        'download_the_clinical_trial_summary': None,
        'brief_summary': 'Brief summary',
        'detailed_description': 'Detailed description',
        'eligibility_criteria': None,
        'start_date': datetime.date(2016, 1, 1),
        'trial_type': 'Study type',
        'trial_design': 'Study design',
        'trial_phase': 'Phase I',
        'ages': None,
    }
