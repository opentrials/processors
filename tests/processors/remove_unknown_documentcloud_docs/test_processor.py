# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.remove_unknown_documentcloud_docs.processor as processor


class TestRemoveUnknownDocumentCloudDocsProcessor(object):
    @mock.patch('documentcloud.DocumentCloud')
    def test_deletes_all_documents_not_in_the_database(self, dc_mock):
        conf = {
            'DOCUMENTCLOUD_USERNAME': 'username',
            'DOCUMENTCLOUD_PASSWORD': 'password',
            'DOCUMENTCLOUD_PROJECT': 'project name',
        }
        conn = {
            'database': mock.Mock()
        }
        document_ids = ['100-foo', '200-bar', '300-baz']
        conn['database'].query.return_value = [
            {'documentcloud_id': '200-bar'},
        ]
        _enable_documentcloud_mock(dc_mock, document_ids)

        processor.process(conf, conn)

        dc_mock().documents.get.assert_has_calls([
            mock.call('300'),
            mock.call().delete(),
            mock.call('100'),
            mock.call().delete(),
        ])

    @mock.patch('documentcloud.DocumentCloud')
    def test_ignores_documents_with_different_titles(self, dc_mock):
        conf = {
            'DOCUMENTCLOUD_USERNAME': 'username',
            'DOCUMENTCLOUD_PASSWORD': 'password',
            'DOCUMENTCLOUD_PROJECT': 'project name',
        }
        conn = {
            'database': mock.Mock()
        }
        document_ids = ['100-foo']
        conn['database'].query.return_value = [
            {'documentcloud_id': '100-bar'},
        ]
        _enable_documentcloud_mock(dc_mock, document_ids)

        processor.process(conf, conn)

        assert not dc_mock().documents.get().delete.called


def _enable_documentcloud_mock(dc_mock, document_ids):
    project = mock.Mock()
    project.document_ids = document_ids

    document = mock.Mock()

    client = mock.Mock()
    client.projects.get_by_title.return_value = project
    client.documents.get.return_value = document

    dc_mock.return_value = client

    return dc_mock
