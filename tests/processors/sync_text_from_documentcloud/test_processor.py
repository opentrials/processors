# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import uuid
import pytest
import processors.sync_text_from_documentcloud.processor as processor


class TestSyncTextFromDocumentCloud(object):

    @mock.patch('documentcloud.DocumentCloud')
    def test_updates_files_with_documentcloud_stripped_pages(self, dc_mock, conn, fda_file):
        conf = {}
        _enable_documentcloud_mock(dc_mock)
        doc_mock = dc_mock.documents.get()
        doc_mock.pages = 3
        doc_mock.get_page_text.side_effect = lambda num: 'page %d\n' % num
        dc_mock().documents.get.return_value = doc_mock

        processor.process(conf, conn)
        updated_file = conn['database']['files'].find_one(id=fda_file)

        assert updated_file['pages'] == ['page 1', 'page 2', 'page 3']


    @mock.patch('documentcloud.DocumentCloud')
    def test_ignores_documents_without_fulltext(self, dc_mock):
        conf = {}
        conn = {
            'database': mock.Mock(),
        }
        conn['database'].query.return_value = [
            {'id': 'file_id', 'documentcloud_id': '100-foo'},
        ]
        dc_mock().documents.get().get_full_text.side_effect = NotImplementedError()

        processor.process(conf, conn)

        conn['database'].update.assert_not_called()

    @mock.patch('documentcloud.DocumentCloud')
    def test_ignores_documents_it_couldnt_load(self, dc_mock):
        conf = {}
        conn = {
            'database': mock.Mock(),
        }
        conn['database'].query.return_value = [
            {'id': 'file_id', 'documentcloud_id': '100-foo'},
        ]
        dc_mock().documents.get.side_effect = Exception()

        processor.process(conf, conn)

    @mock.patch('documentcloud.DocumentCloud')
    def test_raises_stuff(self, dc_mock):
        conf = {}
        conn = {
            'database': mock.Mock(),
        }
        conn['database'].query.return_value = [
            {'id': 'file_id', 'documentcloud_id': '100-foo'},
        ]
        exception = Exception()
        exception.code = 403
        dc_mock().documents.get.side_effect = exception

        with pytest.raises(Exception):
            processor.process(conf, conn)


def _enable_documentcloud_mock(dc_mock):
    project = mock.Mock()

    document = mock.Mock()

    client = mock.Mock()
    client.projects.get_by_title.return_value = project
    client.documents.get.return_value = document

    dc_mock.return_value = client

    return dc_mock
