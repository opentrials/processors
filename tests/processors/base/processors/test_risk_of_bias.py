# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import mock
import processors.base.processors.risk_of_bias as processor


class TestRiskOfBiasProcessor(object):
    @mock.patch('processors.base.processors.risk_of_bias.writers')
    def test_creates_risk_of_bias_if_for_publication(self, writers_mock):
        conn = _get_mock_conn()
        review = {
            'file_name': 'file for publication',
            'source_url': 'source_url',
            'study_id': 'study_id',
        }
        extractors = {
            'extract_source': lambda rev: {},
            'extract_rob': lambda rev, trial_id, source_id: review,
        }
        trial_id = 'trial_id'

        processor.process_risk_of_biases(conn, extractors, review, trial_id)

        writers_mock.write_rob.assert_called_with(conn, review)

    @mock.patch('processors.base.processors.risk_of_bias.writers')
    def test_it_doesnt_create_risk_of_bias_if_not_for_publication(self, writers_mock):
        conn = _get_mock_conn()
        review = {
            'file_name': 'just a file',
            'source_url': 'source_url',
            'study_id': 'study_id',
        }
        extractors = {
            'extract_source': lambda rev: {},
            'extract_rob': lambda rev, trial_id, source_id: review,
        }
        trial_id = 'trial_id'

        processor.process_risk_of_biases(conn, extractors, review, trial_id)

        writers_mock.delete_rob.assert_called_with(conn, review)


def _get_mock_conn():
    return {
        'database': mock.Mock(),
    }
