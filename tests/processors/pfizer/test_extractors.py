# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import pytest
import processors.pfizer.extractors as extractors


class TestPfizerExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @pytest.mark.parametrize('age,expected_min_age,expected_max_age', [
        ('12 Years and older', '12 Years', 'any'),
        ('1 Year-20 Years', '1 Year', '20 Years'),
        ('N/A and older', 'N/A', 'any'),
        (None, None, None),
    ])
    def test_extracts_minimum_and_maximum_ages(self, stub_record, age, expected_min_age, expected_max_age):
        stub_record.update({
            'age_range': age,
        })

        trial = extractors.extract_trial(stub_record)

        assert trial['age_range'] == {
            'min_age': expected_min_age,
            'max_age': expected_max_age,
        }

@pytest.fixture
def stub_record():
    return {
        'nct_id': 'NCT12345678',
        'title': 'Public title',
        'eligibility_criteria': None,
        'study_start_date': datetime.date(2016, 1, 1),
        'gender': 'Both',
        'study_type': 'Study type',
    }
