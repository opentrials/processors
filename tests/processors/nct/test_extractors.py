# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import mock
import pytest
import processors.nct.extractors as extractors


class TestNCTExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)

    @pytest.mark.parametrize('anticipated,actual,result', [
        (500, 200, 500),
        (0, 200, 0),
        (None, 500, 500),
        (None, None, None),
    ])
    def test_target_sample_size(self, anticipated, actual, result, stub_record):
        stub_record.update({
            'enrollment_anticipated': anticipated,
            'enrollment_actual': actual,
        })
        trial = extractors.extract_trial(stub_record)

        assert trial['target_sample_size'] == result

    def test_extracted_identifiers(self, stub_record):
        extracted_trial = extractors.extract_trial(stub_record)

        expected_identifiers = {'nct': 'NCT12345678', 'isrctn': 'ISRCTN71203361'}
        assert extracted_trial['identifiers'] == expected_identifiers

    def test_eligibility_gender_converts_all_to_both(self, stub_record):
        stub_record.update({
            'eligibility': {
                'gender': 'All',
            },
        })
        trial = extractors.extract_trial(stub_record)

        assert trial['gender'] == 'both'

    def test_overall_status_unknown_status(self, stub_record):
        stub_record.update({
            'overall_status': 'Unknown status',
        })
        trial = extractors.extract_trial(stub_record)

        assert trial['status'] == 'unknown'
        assert trial['recruitment_status'] == 'unknown'

    @pytest.mark.parametrize('age,expected_age_call', [
        ('12 Years', '12 Years'),
        (None, None),
    ])
    @mock.patch('processors.base.helpers.format_age', side_effect=lambda x: x)
    def test_extracts_minimum_and_maximum_ages(self, format_age_mock, stub_record, age, expected_age_call):
        stub_record.update({
            'eligibility': {
                'minimum_age': age,
                'maximum_age': age,
            }
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
        'completion_date_actual': datetime.date(2016, 12, 12),
        'results_exemption_date': datetime.date(2016, 11, 9),
        'verification_date': datetime.date(2016, 11, 18),
    }
