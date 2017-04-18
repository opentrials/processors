# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import pytest
import processors.data_contributions.processor as processor

@pytest.mark.usefixtures('enable_betamax')
class TestDataContributionsProcessor(object):
    def test_creates_document_from_contribution(self, conn, data_contribution):
        processor.process({}, conn)

        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        assert conn['database']['documents'].find_one(id=contrib['document_id']) is not None

    def test_links_created_document_with_trial(self, conn, data_contribution):
        processor.process({}, conn)

        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        document = conn['database']['trials_documents'].find_one(
            document_id=contrib['document_id'],
            trial_id=contrib['trial_id']
        )
        assert document is not None

    def test_updates_document_from_contribution(self, conn, data_contribution, document):
        contrib_record = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        document_record = conn['database']['documents'].find_one(id=document)
        contrib_record.update({
            'document_id': document,
        })
        document_record.update({
            'source_url': 'http://example.com',
            'file_id': None,
        })
        conn['explorer']['data_contributions'].update(contrib_record, ['id'])
        conn['database']['documents'].update(document_record, ['id'])
        updated_contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)

        new_contrib_attrs = {
            'url': 'http://www.example.net',
        }
        updated_contrib.update(new_contrib_attrs)
        conn['explorer']['data_contributions'].update(updated_contrib, ['id'])
        processor.process({}, conn)
        updated_document = conn['database']['documents'].find_one(id=document)

        assert updated_document['source_url'] == new_contrib_attrs['url']

    def test_removes_document_if_contribution_is_unapproved(self, conn, data_contribution):
        processor.process({}, conn)

        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        document = conn['database']['documents'].find_one(id=contrib['document_id'])

        contrib.update({'approved': False})
        conn['explorer']['data_contributions'].update(contrib, ['id'])
        processor.process({}, conn)

        assert conn['database']['documents'].find_one(id=document['id']) is None

    def test_updates_contribution_document_id_if_document_is_removed(self, conn, data_contribution):
        processor.process({}, conn)
        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)

        contrib.update({'approved': False})
        conn['explorer']['data_contributions'].update(contrib, ['id'])
        processor.process({}, conn)
        updated_contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)

        assert contrib['document_id'] is not None
        assert updated_contrib['document_id'] is None

    def test_ignores_contribution_with_invalid_url(self, conn, data_contribution):
        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        contrib_attrs = {
            'url': 'invalid url',
        }
        contrib.update(contrib_attrs)
        conn['explorer']['data_contributions'].update(contrib, ['id'])
        processor.process({}, conn)

        updated_contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        assert updated_contrib['document_id'] is None

    def test_ignores_archive_contribution(self, conn, data_contribution):
        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        contrib_attrs = {
            'url': 'https://api.github.com/repos/opentrials/processors/zipball/master',
        }
        contrib.update(contrib_attrs)
        conn['explorer']['data_contributions'].update(contrib, ['id'])
        processor.process({}, conn)

        updated_contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        assert updated_contrib['document_id'] is None

    def test_ignores_contribution_with_invalid_trial_id(self, conn, data_contribution):
        contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        contrib_attrs = {
            'trial_id': 'e0f3ef3c-edba-11e6-ae32-e4b3181a2c8c',
        }
        contrib.update(contrib_attrs)
        conn['explorer']['data_contributions'].update(contrib, ['id'])
        processor.process({}, conn)

        updated_contrib = conn['explorer']['data_contributions'].find_one(id=data_contribution)
        assert updated_contrib['document_id'] is None
