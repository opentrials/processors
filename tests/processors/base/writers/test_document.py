# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import dataset
import sqlalchemy
import uuid
import processors.base.writers as writers


class TestDocumentWriter(object):
    def test_returns_the_document_id(self, conn):
        document = {
            'name': 'name',
            'type': 'csr',
            'source_url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
        }

        document_id = writers.write_document(conn, document)

        assert conn['database']['documents'].find_one(id=document_id)


    def test_writes_file_only_document(self, conn, file_fixture):
        document = {
            'name': 'name',
            'type': 'csr',
            'file_id': file_fixture,
        }

        assert writers.write_document(conn, document) is not None


    def test_writes_url_only_document(self, conn):
        document = {
            'name': 'name',
            'type': 'type',
            'source_url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
        }

        assert writers.write_document(conn, document) is not None


    def test_skips_document_with_invalid_url(self, conn):
        document = {
            'name': 'name',
            'type': 'type',
            'source_url': 'url',
        }

        assert writers.write_document(conn, document) is None


    def test_updates_existing_document_by_id(self, conn):
        original_document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'name': 'name',
            'type': 'csr',
            'source_url': 'http://example.org',
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


    def test_creates_link_with_trial(self, conn, trial):
        document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'trial_id': trial,
            'name': 'name',
            'type': 'csr',
        }

        writers.write_document(conn, document)

        assert conn['database']['trials_documents'].find_one(
            trial_id=document['trial_id'],
            document_id=document['id']
        )


    def test_updates_documents_with_same_type_and_file_id(self, conn, file_fixture):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'file_id': file_fixture,
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert uuid.UUID(new_document_id).hex == document_id


    def test_updates_documents_with_same_type_and_url(self, conn):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'source_url': 'http://example.org',
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert uuid.UUID(new_document_id).hex == document_id


    def test_updates_fda_documents(self, conn, file_fixture, fda_approval):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'type': 'csr',
            'file_id': file_fixture,
            'fda_approval_id': fda_approval,
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)
        assert uuid.UUID(new_document_id).hex == document_id
