# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.base.writers as writers


class TestDocumentWriter(object):
    def test_skips_document_with_invalid_url(self):
        document = {
            'source_id': 'source_id',
            'name': 'name',
            'type': 'type',
            'trial_id': 'trial_id',
            'fda_approval_id': 'fda_approval_id',
            'file_id': 'file_id',
            'url': 'url',
        }
        conn = _get_mock_conn()
        conn['database']['documents'].find_one.return_value = None

        assert writers.write_document(conn, document) is None

    def test_writes_document_with_valid_url(self):
        document = {
            'source_id': 'source_id',
            'name': 'name',
            'type': 'type',
            'trial_id': 'trial_id',
            'fda_approval_id': 'fda_approval_id',
            'file_id': 'file_id',
            'url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
        }
        conn = _get_mock_conn()
        conn['database']['documents'].find_one.return_value = None

        assert writers.write_document(conn, document) is not None


def _get_mock_conn():
    return {
        'database': {
            'documents': mock.Mock(),
        },
    }
