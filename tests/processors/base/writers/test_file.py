# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.base.writers as writers


class TestFileWriter(object):
    def test_skips_file_with_invalid_url(self):
        file_record = {
            'id': '308ec87895f511e68ba9e4b3181a2c8c',
            'sha1': 'd4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4',
            'url': 'url',
        }
        conn = _get_mock_conn()
        conn['database']['files'].find_one.return_value = file_record

        assert writers.write_file(conn, file_record) is None

    def test_writes_file_with_valid_url(self):
        file_record = {
            'id': '308ec87895f511e68ba9e4b3181a2c8c',
            'sha1': 'd4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4',
            'url': 'http://datastore.opentrials.net/documents/fda/d4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4.pdf',
        }
        conn = _get_mock_conn()
        conn['database']['files'].find_one.return_value = file_record

        assert writers.write_file(conn, file_record) is not None


def _get_mock_conn():
    return {
        'database': {
            'files': mock.Mock(),
        },
    }
