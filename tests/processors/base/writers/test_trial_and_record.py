# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import os
import uuid
import mock
import pytest
import sqlalchemy.exc
import processors.base.writers as writers
import processors.base.writers.trial_and_record as trial_and_record_writer


class TestTrialWriter(object):
    def test_creates_new_trial_and_its_record(self, conn, nct_source):
        record_id = uuid.uuid1().hex
        source_url = 'http://example.com/%s' % record_id
        trial = {
            'source_id': nct_source,
            'identifiers': {},
            'public_title': 'title',
        }

        trial_id, _ = writers.write_trial_and_record(conn, trial, record_id, source_url)
        created_trial = conn['database']['trials'].find_one(id=trial_id)
        created_record = conn['database']['records'].find_one(id=record_id)

        assert created_trial['public_title'] == trial['public_title']
        assert created_trial['identifiers'] == trial['identifiers']

        assert created_record['public_title'] == trial['public_title']
        assert created_record['identifiers'] == trial['identifiers']

    def test_it_updates_non_primary_records_values(self, conn, nct_source, euctr_source):
        primary_record_id = uuid.uuid1().hex
        primary_source_url = 'http://example.com/%s' % primary_record_id
        primary_trial = {
            'source_id': nct_source,
            'identifiers': {'nct': 'NCT000001'},
            'public_title': 'title',
        }
        secondary_record_id = uuid.uuid1().hex
        secondary_source_url = 'http://example.com/%s' % secondary_record_id
        secondary_trial = primary_trial.copy()
        secondary_trial['source_id'] = euctr_source

        writers.write_trial_and_record(conn, primary_trial, primary_record_id, primary_source_url)
        _, is_primary = writers.write_trial_and_record(conn, secondary_trial, secondary_record_id, secondary_source_url)

        secondary_record = conn['database']['records'].find_one(id=secondary_record_id)

        assert not is_primary
        assert secondary_record is not None
        for column in secondary_trial.keys():
            assert secondary_record[column] == secondary_trial[column]

    def test_updates_trial_if_new_source_has_higher_priority(self, conn, nct_source, euctr_source, trial, record):
        trial_identifiers = {'euctr': 'EUCTR2005-006078-84'}
        existing_attrs = {
            'id': trial,
            'identifiers': trial_identifiers,
            'source_id': euctr_source,
            'public_title': 'existing title',
        }
        conn['database']['trials'].update(existing_attrs, ['id'])
        record_attrs = {
            'id': record,
            'trial_id': trial,
            'identifiers': trial_identifiers,
            'is_primary': False,
        }
        conn['database']['records'].update(record_attrs, ['id'])

        update_attrs = {
            'source_id': nct_source,
            'identifiers': trial_identifiers,
            'public_title': 'title',
        }

        _, is_primary = writers.write_trial_and_record(
            conn,
            update_attrs,
            record_attrs['id'],
            source_url=None
        )
        updated_trial = conn['database']['trials'].find_one(id=trial)
        updated_record = conn['database']['records'].find_one(id=record)

        assert is_primary
        assert updated_trial['public_title'] == update_attrs['public_title']
        assert updated_record['is_primary']

    def test_it_doesnt_update_trial_if_existing_trial_source_is_higher_priority(self, conn, nct_source, euctr_source, trial, record):
        trial_identifiers = {'nct': 'NCT00212927'}
        existing_attrs = {
            'id': trial,
            'identifiers': trial_identifiers,
            'source_id': nct_source,
            'public_title': 'existing title',
        }
        conn['database']['trials'].update(existing_attrs, ['id'])
        record_attrs = {
            'id': record,
            'trial_id': trial,
            'identifiers': trial_identifiers,
        }
        conn['database']['records'].update(record_attrs, ['id'])

        update_attrs = {
            'source_id': euctr_source,
            'identifiers': trial_identifiers,
            'public_title': 'title',
        }

        _, is_primary = writers.write_trial_and_record(
            conn,
            update_attrs,
            record_attrs['id'],
            source_url=None
        )
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert not is_primary
        assert updated_trial['public_title'] == existing_attrs['public_title']

    def test_it_updates_trial_if_existing_trial_has_no_linked_records(self, conn, nct_source, euctr_source, trial, record):
        '''Bug #389'''
        new_trial_identifiers = {'euctr': 'EUCTR1234-123456-12'}
        existing_trial = {
            'id': trial,
            'identifiers':  {},
            'source_id': nct_source,
            'public_title': 'existing title',
        }
        conn['database']['trials'].update(existing_trial, ['id'])
        existing_record = {
            'id': record,
            'trial_id': trial,
            'identifiers': new_trial_identifiers,
            'source_id': euctr_source,
        }
        conn['database']['records'].update(existing_record, ['id'])
        new_trial = {
            'identifiers': new_trial_identifiers,
            'public_title': 'title',
            'source_id': euctr_source,
        }
        _, is_primary = writers.write_trial_and_record(
            conn,
            new_trial,
            existing_record['id'],
            source_url=None
        )
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert is_primary
        assert updated_trial['identifiers'] == new_trial_identifiers
        assert updated_trial['public_title'] == new_trial['public_title']

    @mock.patch('processors.base.writers.trial_and_record._write_record')
    def test_it_runs_inside_transaction(self, write_record_mock, conn, nct_source):
        record_id = uuid.uuid1().hex
        source_url = 'http://example.com/%s' % record_id
        trial = {
            'source_id': nct_source,
            'identifiers': {},
            'public_title': 'title',
        }
        class CustomException(Exception):
            pass
        write_record_mock.side_effect = CustomException()

        original_trials_count = conn['database']['trials'].count()

        with pytest.raises(CustomException):
            writers.write_trial_and_record(conn, trial, record_id, source_url)

        assert conn['database']['trials'].count() == original_trials_count

    @mock.patch.dict(os.environ, {'SOURCE_COMMIT': 'commit'})
    def test_it_logs_deduplications_with_commit_from_environment(self, conn, nct_source):
        record_id = uuid.uuid1().hex
        source_url = 'http://example.com/%s' % record_id
        trial = {
            'source_id': nct_source,
            'identifiers': {},
            'public_title': 'title',
        }

        trial_id, _ = writers.write_trial_and_record(conn, trial, record_id, source_url)

        log_count = conn['database']['trial_deduplication_logs'].count(
            trial_id=trial_id,
            record_id=record_id,
            commit=os.environ.get('SOURCE_COMMIT'),
            method='initial'
        )

        assert log_count == 1

    @mock.patch('processors.base.writers.trial_and_record.helpers')
    def test_it_doesnt_logs_deduplications_if_latest_log_used_same_dedup_method(self, helpers_mock, conn, nct_source):
        '''This avoids the deduplication logs growing every time we process trials, even if nothing changed.

        We want to log deduplications only when they're different from what
        we've already logged. If the same record was processed 100 times, we
        don't want 100 duplicated rows in the log table. We only want to log if
        something changed. For example, if a trial was previously deduplicated
        via title, but then the source changes its identifiers and now it's
        deduplicated via identifiers.
        '''
        record_id = uuid.uuid1().hex
        source_url = 'http://example.com/%s' % record_id
        trial = {
            'id': uuid.uuid1().hex,
            'identifiers': {'source_id': 'SOURCE000000'},
            'public_title': 'title',
            'source_id': nct_source,
        }
        helpers_mock.find_trial.side_effect = [
            [trial, 'initial'],
            [trial, 'public_title'],
            [trial, 'public_title'],
            [trial, 'identifiers'],
        ]

        writers.write_trial_and_record(conn, trial, record_id, source_url)
        writers.write_trial_and_record(conn, trial, record_id, source_url)
        writers.write_trial_and_record(conn, trial, record_id, source_url)
        writers.write_trial_and_record(conn, trial, record_id, source_url)

        deduplication_logs = conn['database']['trial_deduplication_logs'].find(
            trial_id=trial['id'],
            record_id=record_id,
            order_by='created_at'
        )

        deduplication_methods = [deduplication_log['method'] for deduplication_log in deduplication_logs]
        assert deduplication_methods == ['initial', 'public_title', 'identifiers']

    @mock.patch('processors.base.writers.trial_and_record._write_record')
    def test_it_upserts_all_columns_even_those_not_in_received_trial(self, _, conn, trial):
        record_id = uuid.uuid1().hex
        source_url = 'http://example.com/%s' % record_id
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        simplest_trial = {
            'identifiers': {},
            'public_title': 'title',
            'source_id': trial_attrs['source_id'],
        }
        conn_mock = mock.MagicMock()

        _, is_primary = writers.write_trial_and_record(conn_mock, simplest_trial, record_id, source_url)

        assert is_primary
        conn_mock['database']['trials'].upsert.assert_called()

        upsert_call_args = conn_mock['database']['trials'].upsert.call_args
        upsertted_trial = upsert_call_args[0][0]
        ignored_columns = set(('id', 'created_at', 'updated_at'))

        columns_not_set = list((set(trial_attrs.keys()) - set(upsertted_trial.keys())) - ignored_columns)
        assert columns_not_set == []


class TestRecordWriter(object):
    def test_throws_valueerror_if_record_has_invalid_url(self, conn, trial, nct_source):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        record_id = uuid.uuid1().hex
        invalid_source_url = 'url'

        with pytest.raises(ValueError):
            trial_and_record_writer._write_record(conn, trial_attrs, record_id, nct_source, invalid_source_url, False)

    def test_writes_record_with_valid_url(self, conn, trial, nct_source):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        record_id = uuid.uuid1().hex
        source_url = 'http://example.org/%s' % record_id

        trial_and_record_writer._write_record(conn, trial_attrs, record_id, nct_source, source_url, False)

        assert conn['database']['records'].count(id=record_id) == 1

    def test_doesnt_update_None_parameters(self, conn, trial, record):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        record_attrs = conn['database']['records'].find_one(id=record)

        trial_and_record_writer._write_record(conn, trial_attrs, record, None, None, None)

        updated_record_attrs = conn['database']['records'].find_one(id=record)

        assert record_attrs['source_id'] == updated_record_attrs['source_id']
        assert record_attrs['source_url'] == updated_record_attrs['source_url']
        assert record_attrs['is_primary'] == updated_record_attrs['is_primary']

    def test_sets_is_primary_on_all_other_records_to_false_if_its_the_primary(self, conn, trial):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        record_id = uuid.uuid1().hex
        source_url = 'http://example.org/%s' % record_id

        trial_and_record_writer._write_record(conn, trial_attrs, record_id, trial_attrs['source_id'], source_url, True)

        new_record_id = uuid.uuid1().hex
        new_source_url = 'http://example.org/%s' % new_record_id

        trial_and_record_writer._write_record(conn, trial_attrs, new_record_id, trial_attrs['source_id'], new_source_url, True)

        assert conn['database']['records'].count(id=record_id, is_primary=False) == 1
        assert conn['database']['records'].count(id=new_record_id, is_primary=True) == 1

    def test_doesnt_update_others_is_primary_if_there_was_an_error(self, conn, trial):
        trial_attrs = conn['database']['trials'].find_one(id=trial)
        record_id = uuid.uuid1().hex
        source_url = 'http://example.org/%s' % record_id

        trial_and_record_writer._write_record(conn, trial_attrs, record_id, trial_attrs['source_id'], source_url, True)

        new_record_id = uuid.uuid1().hex
        invalid_source_url = source_url

        with pytest.raises(sqlalchemy.exc.SQLAlchemyError):
            trial_and_record_writer._write_record(conn, trial_attrs, new_record_id, trial_attrs['source_id'], invalid_source_url, True)

        assert conn['database']['records'].count(id=record_id, is_primary=True) == 1

    def test_it_upserts_all_columns_even_those_not_in_received_record(self, conn, trial, record):
        record_attrs = conn['database']['records'].find_one(id=record)
        source_url = 'http://example.com/%s' % record
        conn_mock = mock.MagicMock()
        conn_mock['database']['records'].find_one.return_value = None
        source_id = record_attrs['source_id']
        simplest_trial = {
            'id': trial,
            'identifiers': {},
            'public_title': 'title',
            'source_id': source_id,
        }

        trial_and_record_writer._write_record(conn_mock, simplest_trial, record, source_id, source_url)

        conn_mock['database']['records'].upsert.assert_called()

        upsert_call_args = conn_mock['database']['records'].upsert.call_args
        upsertted_record = upsert_call_args[0][0]
        ignored_columns = set(('id', 'created_at', 'updated_at'))

        columns_not_set = list((set(record_attrs.keys()) - set(upsertted_record.keys())) - ignored_columns)
        assert columns_not_set == []
