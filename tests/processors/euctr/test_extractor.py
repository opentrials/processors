# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import datetime
import pytest
import processors.euctr.extractors as extractors


class TestEUCTRExtractors(object):
    def test_stub_record_is_valid(self, stub_record):
        extractors.extract_trial(stub_record)


    @pytest.mark.parametrize('male, female, expected_gender', [
        (True, None, 'male'),
        (True, True, 'both'),
        (True, False, 'male'),
    ])
    def test_extract_gender_for_trial(self, stub_record, male, female, expected_gender):
        stub_record.update({
            'subject_male': male,
            'subject_female': female,
        })
        trial = extractors.extract_trial(stub_record)

        assert trial['gender'] == expected_gender


    @pytest.mark.parametrize('identifiers, expected_identifiers', [
        (
            {
                'eudract_number': '2013-030180-02',
                'us_nct_clinicaltrials_gov_registry_number': 'NCT00020500',
            },
            {
                'nct': 'NCT00020500',
                'euctr': 'EUCTR2013-030180-02',
            }
        ),
    ])
    def test_extracted_identifiers_for_trial(self, stub_record, identifiers, expected_identifiers):
        stub_record.update(identifiers)
        extracted_trial = extractors.extract_trial(stub_record)

        assert extracted_trial['identifiers'] == expected_identifiers


    @pytest.mark.parametrize('status, expected_status, expected_rec_status', [
        (None, None, None),
        ('Completed', 'complete', 'not_recruiting'),
    ])
    def test_extract_status_for_trial(self, stub_record, status, expected_status, expected_rec_status):
        stub_record.update({ 'trial_status': status })
        extracted_trial = extractors.extract_trial(stub_record)

        assert extracted_trial['status'] == expected_status
        assert extracted_trial['recruitment_status'] == expected_rec_status


    @pytest.mark.parametrize('trial_results_url, has_published_results', [
        (None, False),
        ('https://www.clinicaltrialsregister.eu/ctr-search/trial/2015-004907-22/results', True),
    ])
    def test_trial_has_published_results(self, stub_record, trial_results_url, has_published_results):
        stub_record.update({ 'trial_results_url': trial_results_url })
        extracted_trial = extractors.extract_trial(stub_record)

        assert extracted_trial['has_published_results'] == has_published_results


    @pytest.mark.parametrize('trial_results_url', [
        'https://www.clinicaltrialsregister.eu/ctr-search/trial/2015-004907-22/result',
    ])
    def test_extract_document_if_trial_results_url(self, stub_record, trial_results_url):
        stub_record.update({ 'trial_results_url': trial_results_url })
        extracted_documents = extractors.extract_documents(stub_record)

        assert extracted_documents[0]['source_url'] == trial_results_url


@pytest.fixture
def stub_record():
    return {
        'eudract_number': '2013-030180-02',
        'us_nct_clinicaltrials_gov_registry_number': 'NCT00020500',
        'isrctn_international_standard_randomised_controlled_trial_numbe': None,
        'who_universal_trial_reference_number_utrn': None,
        'title_of_the_trial_for_lay_people_in_easily_understood_i_e_non_': 'Title',
        'eudract_number_with_country': '2013-030180-02/IT',
        'full_title_of_the_trial': 'Full title of trial',
        'trial_status': 'Completed',
        'subject_female': True,
        'subject_male': True,
        'trial_results': 'View results',
        'trial_results_url': 'https://www.clinicaltrialsregister.eu/ctr-search/trial/2015-004907-22/results',
        'trial_main_objective_of_the_trial': 'Heal everybody',
        'date_on_which_this_record_was_first_entered_in_the_eudract_data': datetime.datetime(2012, 1, 1),
        'date_of_the_global_end_of_the_trial': datetime.datetime(2016, 1, 1),
        'public_title': 'Public title of trial',
        'trial_principal_inclusion_criteria': 'everybody',
        'trial_principal_exclusion_criteria': 'nobody',
        'subject_in_the_whole_clinical_trial': 12,
        'target_sample_size': 10000000,
        'first_enrollment_date': None,
    }
