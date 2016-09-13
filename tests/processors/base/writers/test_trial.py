# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import mock
import processors.base.writers as writers


class TestTrialWriter(object):
    @mock.patch('processors.base.writers.trial.helpers')
    def test_creates_new_trial(self, helpers_mock):
        conn = _get_mock_conn()
        trial = {
            'identifiers': {},
            'public_title': 'title',
        }
        source_id = 'source_id'
        record_id = 'record_id'
        helpers_mock.find_trial_by_identifiers.return_value = None

        result, _ = writers.write_trial(conn, trial, source_id, record_id)

        conn['database']['trials'].upsert.assert_called()
        args = conn['database']['trials'].upsert.call_args
        created_trial, keys = args[0]
        kwargs = args[1]

        assert created_trial['id'] == result
        assert created_trial['public_title'] == trial['public_title']
        assert created_trial['identifiers'] == trial['identifiers']
        assert created_trial['created_at'] is not None
        assert keys == ['id']
        assert kwargs == {'ensure': False}

    @mock.patch('processors.base.writers.trial.helpers')
    def test_updates_trial_if_new_source_has_higher_priority(self, helpers_mock):
        conn = _get_mock_conn()
        trial = {
            'identifiers': {},
            'public_title': 'title',
        }
        source_id = 'nct'
        record_id = 'record_id'
        existing_trial = {
            'id': '7003e8c7-7e66-4655-bb51-efcf0481a3ee',
            'public_title': 'existing title',
            'source_id': 'euctr',
        }
        helpers_mock.find_trial_by_identifiers.return_value = existing_trial.copy()

        result, is_primary = writers.write_trial(conn, trial, source_id, record_id)

        conn['database']['trials'].upsert.assert_called()
        args = conn['database']['trials'].upsert.call_args
        created_trial = args[0][0]

        assert is_primary
        assert created_trial['id'] == existing_trial['id']
        assert created_trial['public_title'] == trial['public_title']

    @mock.patch('processors.base.writers.trial.helpers')
    def test_it_doesnt_update_trial_if_existing_trial_source_is_higher_priority(self, helpers_mock):
        conn = _get_mock_conn()
        trial = {
            'identifiers': {},
            'public_title': 'title',
        }
        source_id = 'euctr'
        record_id = 'record_id'
        existing_trial = {
            'id': '7003e8c7-7e66-4655-bb51-efcf0481a3ee',
            'public_title': 'existing title',
            'source_id': 'nct',
        }
        helpers_mock.find_trial_by_identifiers.return_value = existing_trial.copy()

        result, is_primary = writers.write_trial(conn, trial, source_id, record_id)

        conn['database']['trials'].upsert.assert_called()
        args = conn['database']['trials'].upsert.call_args
        created_trial = args[0][0]

        assert not is_primary
        assert created_trial['public_title'] == existing_trial['public_title']

    @mock.patch('processors.base.writers.trial.helpers')
    def test_it_updates_trial_if_existing_trial_has_no_linked_records(self, helpers_mock):
        '''Bug #389'''
        conn = _get_mock_conn()
        trial = {
            'identifiers': {},
            'public_title': 'title',
        }
        source_id = 'source_id'
        record_id = 'record_id'
        existing_trial = {
            'id': '7003e8c7-7e66-4655-bb51-efcf0481a3ee',
            'public_title': 'existing title',
            'source_id': 'nct',
        }
        helpers_mock.find_trial_by_identifiers.return_value = existing_trial.copy()
        conn['database']['records'].count.return_value = 0

        result, is_primary = writers.write_trial(conn, trial, source_id, record_id)

        assert is_primary
        conn['database']['records'].count.assert_called_with(
            trial_id=existing_trial['id'],
            source_id=existing_trial['source_id']
        )


def _get_mock_conn():
    return {
        'database': {
            'trials': mock.Mock(),
            'records': mock.Mock(),
        },
    }
