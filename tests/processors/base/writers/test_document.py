# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import dataset
import sqlalchemy
import processors.base.writers as writers


class TestDocumentWriter(object):
    def test_returns_the_document_id(self, conn):
        document = {
            'name': 'name',
            'type': 'csr',
            'file_id': '7e7bee65ba2b4adba3657d88ad1afc3f',
            'url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
        }

        document_id = writers.write_document(conn, document)

        assert conn['database']['documents'].find_one(id=document_id)

    def test_writes_file_only_document(self, conn):
        document = {
            'name': 'name',
            'type': 'csr',
            'file_id': '7e7bee65ba2b4adba3657d88ad1afc3f',
        }

        assert writers.write_document(conn, document) is not None

    def test_writes_url_only_document(self, conn):
        document = {
            'name': 'name',
            'type': 'type',
            'url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
        }

        assert writers.write_document(conn, document) is not None

    def test_skips_document_with_invalid_url(self, conn):
        document = {
            'name': 'name',
            'type': 'type',
            'url': 'url',
        }

        assert writers.write_document(conn, document) is None

    def test_updates_existing_document_by_id(self, conn):
        original_document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'name': 'name',
            'type': 'csr',
            'url': 'http://example.org',
        }
        new_document = {
            'id': original_document['id'],
            'name': 'new name',
            'type': 'results',
        }
        table = conn['database']['documents']
        table.insert(original_document)

        writers.write_document(conn, new_document)

        document = table.find_one(id=original_document['id'])

        assert document['name'] == new_document['name']
        assert document['type'] == new_document['type']

    def test_creates_link_with_trial(self, conn):
        document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'trial_id': '7b77a80a8e0541aa92a02ef27d45a0ac',
            'name': 'name',
            'type': 'csr',
        }

        writers.write_document(conn, document)

        assert conn['database']['trials_documents'].find_one(
            trial_id=document['trial_id'],
            document_id=document['id']
        )

    def test_updates_documents_with_same_type_and_file_id(self, conn):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'file_id': '7e7bee65ba2b4adba3657d88ad1afc3f',
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert new_document_id == document_id

    def test_updates_documents_with_same_type_and_url(self, conn):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'url': 'http://example.org',
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert new_document_id == document_id

    def test_updates_fda_documents(self, conn):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'file_id': '7e7bee65ba2b4adba3657d88ad1afc3f',
            'fda_approval_id': 'd263061170d84b41bcebfb03582e84b9',
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)
        assert new_document_id == document_id


@pytest.fixture
def conn():
    db = dataset.connect('sqlite:///:memory:')
    db.create_table('documents', primary_type='String')
    db.create_table('trials', primary_type='String')
    db.create_table('trials_documents')

    _create_str_columns(db['documents'], [
        'name',
        'type',
        'file_id',
        'trial_id',
        'fda_approval_id',
        'url',
    ])

    _create_str_columns(db['trials_documents'], [
        'trial_id',
        'document_id',
    ])

    return {
        'database': db,
    }


def _create_str_columns(table, columns):
    for column in columns:
        table.create_column(column, sqlalchemy.String)
