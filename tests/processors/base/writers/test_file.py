# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import processors.base.writers as writers


class TestFileWriter(object):
    def test_skips_file_with_invalid_url(self, conn):
        file_record = {
            'id': '308ec87895f511e68ba9e4b3181a2c8c',
            'sha1': 'd4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4',
            'source_url': 'url',
        }

        assert writers.write_file(conn, file_record) is None


    def test_writes_file_with_valid_url(self, conn):
        file_record = {
            'id': '308ec87895f511e68ba9e4b3181a2c8c',
            'sha1': 'd4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4',
            'source_url': 'http://datastore.opentrials.net/documents/fda/d4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4.pdf',
        }

        assert writers.write_file(conn, file_record) is not None


    def test_keeps_the_files_current_attributes(self, conn):
        file_record = {
            'id': '308ec878-95f5-11e6-8ba9-e4b3181a2c8c',
            'sha1': 'd4bac000bb4a42d8c9e3a8679bc5f8fd571b3ba4',
            'source_url': 'http://example.org',
            'documentcloud_id': '1000',
            'pages': ['page 1', 'page 2'],
        }
        writers.write_file(conn, file_record)
        writers.write_file(conn, {'id': file_record['id']})
        upserted_file = conn['database']['files'].find_one(id=file_record['id'])

        assert upserted_file == file_record
