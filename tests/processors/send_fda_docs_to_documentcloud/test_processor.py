# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import mock
import datetime
import pytest
import sqlalchemy
import documentcloud
import dataset
import processors.send_fda_docs_to_documentcloud.processor as processor

SendFDADocsToDocumentCloudProcessor = processor._SendFDADocsToDocumentCloudProcessor


class TestSendFDADocsToDocumentCloudProcessor(object):
    CONF = {
        'DOCUMENTCLOUD_USERNAME': 'username',
        'DOCUMENTCLOUD_PASSWORD': 'username',
        'DOCUMENTCLOUD_PROJECT': 'username',
    }


    @mock.patch('documentcloud.DocumentCloud')
    def test_process_file(self, dc_mock, file_stub, conn):
        doc_mock, project_mock = _setup_documentcloud_mock(dc_mock)
        doc_mock.file_hash = file_stub['sha1']
        application_type = re.match(r'^[A-Z]+', file_stub['fda_application_id']).group(0)

        processor = SendFDADocsToDocumentCloudProcessor(self.CONF, conn['database'])
        processor.process_file(file_stub)

        doc_mock.save.assert_called()
        assert doc_mock.project == project_mock
        assert doc_mock.access == 'public'
        assert doc_mock.data == {
            'fda_application': file_stub['fda_application_id'],
            'application_type': application_type,
            'supplement_number': str(file_stub['supplement_number']),
            'name': file_stub['name'],
            'type': file_stub['type'],
            'action_date': file_stub['action_date'].isoformat(),
        }


    @mock.patch('documentcloud.DocumentCloud')
    def test_doesnt_upload_file_if_it_wasnt_modified(self, dc_mock, file_stub, conn):
        doc_mock, project_mock = _setup_documentcloud_mock(dc_mock)
        doc_mock.file_hash = file_stub['sha1']

        processor = SendFDADocsToDocumentCloudProcessor(self.CONF, conn['database'])
        processor.process_file(file_stub)

        dc_mock().documents.upload.assert_not_called()


    @mock.patch('documentcloud.DocumentCloud')
    def test_uploads_and_remove_old_file_if_it_was_modified(self, dc_mock, file_stub, conn):
        doc_mock, project_mock = _setup_documentcloud_mock(dc_mock)
        doc_mock.file_hash = 'different-hash'

        processor = SendFDADocsToDocumentCloudProcessor(self.CONF, conn['database'])
        processor.process_file(file_stub)

        doc_mock.delete.assert_called()
        dc_mock().documents.upload.assert_called()


    @mock.patch('documentcloud.DocumentCloud')
    def test_doesnt_remove_file_if_it_has_no_file_hash(self, dc_mock, file_stub, conn):
        '''A recently-uploaded document to DC has no file_hash.'''
        del file_stub['documentcloud_id']
        doc_mock, project_mock = _setup_documentcloud_mock(dc_mock)
        doc_mock.file_hash = None

        processor = SendFDADocsToDocumentCloudProcessor(self.CONF, conn['database'])
        processor.process_file(file_stub)

        doc_mock.delete.assert_not_called()
        dc_mock().documents.upload.assert_called()


@pytest.fixture
def file_stub(conn, fda_document):
    document_record = conn['database']['documents'].find_one(id=fda_document)
    file_record = conn['database']['files'].find_one(id=document_record['file_id'])
    fda_approval_record = conn['database']['fda_approvals'].find_one(id=document_record['fda_approval_id'])

    return {
        'id': file_record['id'],
        'documentcloud_id': file_record['documentcloud_id'],
        'sha1': file_record['sha1'],
        'fda_application_id': fda_approval_record['fda_application_id'],
        'supplement_number': fda_approval_record['supplement_number'],
        'type': fda_approval_record['type'],
        'name': document_record['name'],
        'source_url': file_record['source_url'],
        'action_date': fda_approval_record['action_date'],
    }


def _setup_documentcloud_mock(dc_mock):
    project_mock = mock.Mock(autospec=documentcloud.Project)
    dc_mock().projects.get_or_create_by_title.return_value = [project_mock, None]

    doc_mock = mock.Mock(autospec=documentcloud.Document)
    doc_mock.id = '123456-document-title'
    dc_mock().documents.get.return_value = doc_mock
    dc_mock().documents.upload.return_value = doc_mock

    return doc_mock, project_mock
