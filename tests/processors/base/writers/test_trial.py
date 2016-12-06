# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import pytest
import processors.base.writers as writers


class TestTrialWriter(object):
    def test_creates_new_trial(self, conn, nct_source, record):
        trial = {
            'identifiers': {},
            'public_title': 'title',
        }

        result, _ = writers.write_trial(conn, trial, nct_source, record)
        created_trial = conn['database']['trials'].find_one(id=result)

        assert created_trial['public_title'] == trial['public_title']
        assert created_trial['identifiers'] == trial['identifiers']
        assert created_trial['created_at'] is not None

    def test_updates_trial_if_new_source_has_higher_priority(self,
        conn, nct_source, euctr_source, trial, record):

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
        }
        conn['database']['records'].update(record_attrs, ['id'])

        update_attrs = {
            'identifiers': trial_identifiers,
            'public_title': 'title',
        }

        result, is_primary = writers.write_trial(conn, update_attrs, nct_source, record)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert is_primary
        assert updated_trial['public_title'] == update_attrs['public_title']

    def test_it_doesnt_update_trial_if_existing_trial_source_is_higher_priority(self,
        conn, nct_source, euctr_source, trial, record):

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
            'identifiers': trial_identifiers,
            'public_title': 'title',
        }

        result, is_primary = writers.write_trial(conn, update_attrs, euctr_source, record)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert not is_primary
        assert updated_trial['public_title'] == existing_attrs['public_title']

    def test_it_updates_trial_if_existing_trial_has_no_linked_records(self, conn,
        nct_source, euctr_source, trial, record):
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
        result, is_primary = writers.write_trial(conn, new_trial, euctr_source, record)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert is_primary
        assert updated_trial['identifiers'] == new_trial_identifiers
        assert updated_trial['public_title'] == new_trial['public_title']
