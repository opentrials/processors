# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import uuid
import datetime
import collections
import processors.merge_trials_identifiers.processor as processor


class TestMergeTrialIdentifiersProcessor(object):
    @mock.patch('datetime.datetime')
    def test_updates_trial_with_records_identifiers(self, datetime_mock):
        query_result = [
            {
                'id': uuid.uuid1(),
                'trial_identifiers': {},
                'records_identifiers': {'nct': 'NCT11111', 'ictrp': 'ICTRP000000'},
            },
        ]
        db_mock = mock.MagicMock()
        db_mock['trials'] = mock.Mock()
        db_mock.query.return_value = query_result
        datetime_mock.utcnow.return_value = 'the_date'

        conf = {}
        conn = {'database': db_mock}
        processor.process(conf, conn)

        expected_trial = {
            'id': query_result[0]['id'].hex,
            'identifiers': query_result[0]['records_identifiers'],
            'updated_at': datetime.datetime.utcnow(),
        }

        db_mock['trials'].update.assert_called_with(expected_trial, ['id'])

    def test_merges_identifiers(self):
        query_result = [
            {
                'id': uuid.uuid1(),
                'trial_identifiers': {'nct': 'NCT000000'},
                'records_identifiers': {'ictrp': 'ICTRP000000'},
            },
        ]
        db_mock = mock.MagicMock()
        db_mock['trials'] = mock.Mock()
        db_mock.query.return_value = query_result

        conf = {}
        conn = {'database': db_mock}
        processor.process(conf, conn)

        expected_identifiers = {'nct': 'NCT000000', 'ictrp': 'ICTRP000000'}
        updated_trial, _ = db_mock['trials'].update.call_args[0]
        assert updated_trial.get('identifiers') == expected_identifiers

    def test_it_uses_records_identifiers_when_there_are_multiple_ids_from_same_source(self):
        query_result = [
            {
                'id': uuid.uuid1(),
                'trial_identifiers': {'nct': 'NCT00000'},
                'records_identifiers': {'nct': 'NCT11111'},
            },
        ]
        db_mock = mock.MagicMock()
        db_mock['trials'] = mock.Mock()
        db_mock.query.return_value = query_result

        conf = {}
        conn = {'database': db_mock}
        processor.process(conf, conn)

        expected_identifiers = query_result[0]['records_identifiers']
        updated_trial, _ = db_mock['trials'].update.call_args[0]
        assert updated_trial.get('identifiers') == expected_identifiers

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
