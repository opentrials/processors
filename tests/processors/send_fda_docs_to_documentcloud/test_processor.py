# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
        file_stub['fda_application_id'] = 'NDA00000-000'

        processor = SendFDADocsToDocumentCloudProcessor(self.CONF, conn['database'])
        processor.process_file(file_stub)

        doc_mock.save.assert_called()
        assert doc_mock.project == project_mock
        assert doc_mock.access == 'public'
        assert doc_mock.data == {
            'fda_application': file_stub['fda_application_id'],
            'application_type': 'NDA',
            'supplement_number': str(file_stub['supplement_number']),
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
def file_stub():
    return {
        'documentcloud_id': 'dc_id',
        'sha1': 'sha1',
        'fda_application_id': 'NDA000000-000',
        'supplement_number': 0,
        'type': 'Review',
        'name': 'Review',
        'url': 'https://example.org/file.pdf',
        'action_date': datetime.date(2016, 1, 1),
    }


@pytest.fixture
def conn():
    db = dataset.connect('sqlite:///:memory:')
    _create_str_columns(db['files'], [
        'documentcloud_id',
        'sha1',
        'fda_application_id',
        'type',
        'name',
        'url',
    ])
    db['files'].create_column('supplement_number', sqlalchemy.Integer)
    db['files'].create_column('action_date', sqlalchemy.Date)

    return {
        'database': db,
    }


def _setup_documentcloud_mock(dc_mock):
    project_mock = mock.Mock(autospec=documentcloud.Project)
    dc_mock().projects.get_or_create_by_title.return_value = [project_mock, None]

    doc_mock = mock.Mock(autospec=documentcloud.Document)
    doc_mock.id = '123456-document-title'
    dc_mock().documents.get.return_value = doc_mock
    dc_mock().documents.upload.return_value = doc_mock

    return doc_mock, project_mock


def _create_str_columns(table, columns):
    for column in columns:
        table.create_column(column, sqlalchemy.String)
