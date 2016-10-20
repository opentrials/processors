# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.base.writers as writers


class TestRecordWriter(object):
    def test_skips_record_with_invalid_url(self):
        record = {
            'meta_id': 'meta_id',
            'meta_created': '2016-05-26 05:42:33.555790 +03:00',
            'meta_updated': '2016-05-26 05:42:33.555790 +03:00',
            'meta_source': 'url',
        }
        trial = {
            'identifiers': {},
            'public_title': 'public_title',
        }
        trial_id = 'trial_id'
        source_id = 'source_id'
        conn = _get_mock_conn()
        conn['database']['records'].find_one.return_value = None

        assert writers.write_record(conn, record, source_id, trial_id, trial) is None

    def test_writes_record_with_valid_url(self):
        record = {
            'meta_id': 'meta_id',
            'meta_created': '2016-05-26 05:42:33.555790 +03:00',
            'meta_updated': '2016-05-26 05:42:33.555790 +03:00',
            'meta_source': 'http://www.pfizer.com/research/clinical_trials/find_a_trial/NCT00666575',
        }
        trial = {
            'identifiers': {},
            'public_title': 'public_title',
        }
        trial_id = 'trial_id'
        source_id = 'source_id'
        conn = _get_mock_conn()
        conn['database']['records'].find_one.return_value = None

        assert writers.write_record(conn, record, source_id, trial_id, trial) is not None


def _get_mock_conn():
    return {
        'database': {
            'records': mock.Mock(),
        },
    }
