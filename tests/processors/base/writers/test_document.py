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
    def test_returns_the_document_id(self, conn, document_category):
        document = {
            'name': 'name',
            'source_url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
            'document_category_id': document_category,
        }

        document_id = writers.write_document(conn, document)

        assert conn['database']['documents'].find_one(id=document_id)


    def test_writes_file_only_document(self, conn, file_fixture, document_category):
        document = {
            'name': 'name',
            'file_id': file_fixture,
            'document_category_id': document_category,
        }

        assert writers.write_document(conn, document) is not None


    def test_writes_url_only_document(self, conn, document_category):
        document = {
            'name': 'name',
            'source_url': 'https://clinicaltrials.gov/ct2/show/results/NCT00486265',
            'document_category_id': document_category,
        }

        assert writers.write_document(conn, document) is not None


    def test_skips_document_with_invalid_url(self, conn, document_category):
        document = {
            'name': 'name',
            'source_url': 'url',
            'document_category_id': document_category,
        }

        assert writers.write_document(conn, document) is None


    def test_updates_existing_document_by_id(self, conn, document_category):
        original_document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'name': 'name',
            'source_url': 'http://example.org',
            'document_category_id': document_category,
        }
        new_document = {
            'id': original_document['id'],
            'name': 'new name',
            'source_url': 'http://example.net',
            'document_category_id': document_category,
        }
        table = conn['database']['documents']
        table.insert(original_document)

        writers.write_document(conn, new_document)

        document = table.find_one(id=original_document['id'])

        assert document['name'] == new_document['name']
        assert document['source_url'] == new_document['source_url']


    def test_creates_link_with_trial(self, conn, trial, document_category):
        document = {
            'id': '5b99281096b311e6a0ecf8165487599c',
            'trial_id': trial,
            'source_url': 'http://example.com',
            'name': 'name',
            'document_category_id': document_category,
        }

        writers.write_document(conn, document)

        assert conn['database']['trials_documents'].find_one(
            trial_id=document['trial_id'],
            document_id=document['id']
        )


    def test_updates_documents_with_same_type_and_file_id(self, conn, file_fixture, document_category):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'file_id': file_fixture,
            'document_category_id': document_category,
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert uuid.UUID(new_document_id).hex == document_id


    def test_updates_documents_with_same_type_and_url(self, conn, document_category):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'source_url': 'http://example.org',
            'document_category_id': document_category,
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)

        assert uuid.UUID(new_document_id).hex == document_id


    def test_updates_fda_documents(self, conn, file_fixture, fda_approval, document_category):
        document_id = '5b99281096b311e6a0ecf8165487599c'
        document = {
            'id': document_id,
            'name': 'name',
            'file_id': file_fixture,
            'fda_approval_id': fda_approval,
            'document_category_id': document_category,
        }
        writers.write_document(conn, document)

        del document['id']

        new_document_id = writers.write_document(conn, document)
        assert uuid.UUID(new_document_id).hex == document_id
