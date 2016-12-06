# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import uuid
import datetime
import collections
from copy import deepcopy
import processors.merge_trials_identifiers.processor as processor


class TestMergeTrialIdentifiersProcessor(object):
    def test_updates_trial_with_records_identifiers(self, conn, trial, record):
        trial_attrs = {
            'id': trial,
            'identifiers': {},
        }
        conn['database']['trials'].update(trial_attrs, ['id'])
        trial_last_updated = datetime.datetime.utcnow()
        record_attrs = {
            'id': record,
            'trial_id': trial,
            'identifiers': {'nct': 'NCT11111', 'ictrp': 'ICTRP000000'},
        }
        conn['database']['records'].update(record_attrs, ['id'])

        processor.process({}, conn)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert updated_trial['identifiers'] == record_attrs['identifiers']
        assert updated_trial['updated_at'].replace(tzinfo=None) > trial_last_updated


    def test_merges_identifiers(self, conn, trial, record):
        trial_attrs = {
            'id': trial,
            'identifiers': {'nct': 'NCT87654321'},
        }
        conn['database']['trials'].update(trial_attrs, ['id'])
        trial_last_updated = datetime.datetime.utcnow()
        record_attrs = {
            'id': record,
            'trial_id': trial ,
            'identifiers': {'isrctn': 'ISRCTN71203361'},
        }
        conn['database']['records'].update(record_attrs, ['id'])
        expected_identifiers = deepcopy(record_attrs['identifiers'])
        expected_identifiers.update(trial_attrs['identifiers'])

        processor.process({}, conn)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert updated_trial['identifiers'] == expected_identifiers
        assert updated_trial['updated_at'].replace(tzinfo=None) > trial_last_updated


    def test_it_uses_records_identifiers_when_there_are_multiple_ids_from_same_source(self,
        conn, trial, record):
        trial_attrs = {
            'id': trial,
            'identifiers': {'nct': 'NCT87654321'},
        }
        conn['database']['trials'].update(trial_attrs, ['id'])
        record_attrs = {
            'id': record,
            'trial_id': trial ,
            'identifiers': {'nct': 'NCT12345678'},
        }
        conn['database']['records'].update(record_attrs, ['id'])

        processor.process({}, conn)
        updated_trial = conn['database']['trials'].find_one(id=trial)

        assert updated_trial['identifiers'] == record_attrs['identifiers']


    def test_doesnt_update_identifiers_if_theyre_a_subset_of_the_trials_identifiers(self):
        query_result = [
            {
                'id': uuid.uuid1(),
                'trial_identifiers': {'nct': 'NCT00000', 'ictrp': 'ICTRP0000000'},
                'records_identifiers': {'ictrp': 'ICTRP0000000'},
            },
        ]
        db_mock = mock.MagicMock()
        db_mock['trials'] = mock.Mock()
        db_mock.query.return_value = query_result

        conf = {}
        conn = {'database': db_mock}
        processor.process(conf, conn)

        db_mock['trials'].update.assert_not_called()


    def test_ignores_identifiers_order(self):
        trial_identifiers = collections.OrderedDict([
            ('nct', 'NCT000000'),
            ('drks', 'DRKS0000000'),
        ])
        record_identifiers = collections.OrderedDict([
            ('drks', 'DRKS0000000'),
            ('nct', 'NCT000000'),
        ])
        assert trial_identifiers.items() != record_identifiers.items(), \
            'Identifiers items must be different unless sorted'
        query_result = [
            {
                'id': uuid.uuid1(),
                'trial_identifiers': trial_identifiers,
                'records_identifiers': record_identifiers,
            },
        ]
        db_mock = mock.MagicMock()
        db_mock['trials'] = mock.Mock()
        db_mock.query.return_value = query_result

        conf = {}
        conn = {'database': db_mock}
        processor.process(conf, conn)

        db_mock['trials'].update.assert_not_called()
