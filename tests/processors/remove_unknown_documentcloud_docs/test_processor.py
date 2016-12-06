# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.remove_unknown_documentcloud_docs.processor as processor


class TestRemoveUnknownDocumentCloudDocsProcessor(object):
    @mock.patch('documentcloud.DocumentCloud')
    def test_deletes_all_documents_not_in_the_database(self, dc_mock, conn, fda_file):
        file_attrs = {
            'id': fda_file,
            'documentcloud_id': '200-bar',
        }
        conn['database']['files'].update(file_attrs, ['id'])
        remote_document_ids = ['100-foo', '200-bar', '300-baz']
        conf = {
            'DOCUMENTCLOUD_USERNAME': 'username',
            'DOCUMENTCLOUD_PASSWORD': 'password',
            'DOCUMENTCLOUD_PROJECT': 'project name',
        }
        _enable_documentcloud_mock(dc_mock, remote_document_ids)

        processor.process(conf, conn)

        dc_mock().documents.delete.assert_has_calls([
            mock.call('300'),
            mock.call('100'),
        ])


    @mock.patch('documentcloud.DocumentCloud')
    def test_ignores_documents_with_different_titles(self, dc_mock, conn, fda_file):
        file_attrs = {
            'id': fda_file,
            'documentcloud_id': '100-bar',
        }
        conn['database']['files'].update(file_attrs, ['id'])
        remote_document_ids = ['100-foo']
        conf = {
            'DOCUMENTCLOUD_USERNAME': 'username',
            'DOCUMENTCLOUD_PASSWORD': 'password',
            'DOCUMENTCLOUD_PROJECT': 'project name',
        }
        _enable_documentcloud_mock(dc_mock, remote_document_ids)

        processor.process(conf, conn)

        assert not dc_mock().documents.get().delete.called


def _enable_documentcloud_mock(dc_mock, document_ids):
    project = mock.Mock()
    project.document_ids = document_ids

    client = mock.Mock()
    client.projects.get_by_title.return_value = project

    dc_mock.return_value = client

    return dc_mock
