# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import processors.base.helpers as helpers
import processors.pubmed_unregistered_trials.processor as processor
import processors.pubmed_unregistered_trials.extractors as extractors_module


class TestPubmedUnregisteredTrialsProcessor(object):
    def test_creates_unregistred_trial_if_no_registry_ids(self, conn, pubmed_record):
        conn['warehouse']['pubmed'].update(
            {
                'pmid': pubmed_record,
                'registry_ids': None,
            },
            ['pmid']
        )
        identifiers = {'pubmed': ('PUBMED%s' % pubmed_record)}
        processor.process({}, conn)

        trial = helpers.find_trial_by_identifiers(conn, identifiers)
        assert trial is not None


    def test_creates_document_if_trial_found_from_registry_ids(self, conn,
        pubmed_record, record, trial, results_document_category):

        identifiers = {'isrctn': 'ISRCTN31181395'}
        conn['database']['records'].update(
            {
                'id': record,
                'identifiers': identifiers,
                'trial_id': trial,
            },
            ['id']
        )
        pubmed_attrs = conn['warehouse']['pubmed'].find_one(pmid=pubmed_record)
        pubmed_attrs['registry_ids'] = [identifiers]
        conn['warehouse']['pubmed'].update(pubmed_attrs, ['pmid'])
        processor.process({}, conn)

        document = conn['database']['documents'].find_one(
            source_url=pubmed_attrs['meta_source']
        )
        assert document is not None


    def test_links_results_document_to_found_trial(self, conn,
        pubmed_record, record, trial, results_document_category):

        identifiers = {'isrctn': 'ISRCTN31181395'}
        conn['database']['records'].update(
            {
                'id': record,
                'identifiers': identifiers,
                'trial_id': trial,
            },
            ['id']
        )
        pubmed_attrs = conn['warehouse']['pubmed'].find_one(pmid=pubmed_record)
        pubmed_attrs['registry_ids'] = [identifiers]
        conn['warehouse']['pubmed'].update(pubmed_attrs, ['pmid'])
        processor.process({}, conn)

        document = conn['database']['documents'].find_one(
            source_url=pubmed_attrs['meta_source']
        )
        trial_document = conn['database']['trials_documents'].find_one(
            trial_id=trial, document_id=document['id']
        )
        assert trial_document is not None


    def test_doesnt_create_document_if_trial_not_found_from_registry_ids(self, conn,
        pubmed_record):

        pubmed_attrs = conn['warehouse']['pubmed'].find_one(pmid=pubmed_record)
        pubmed_attrs['registry_ids'] = [{'isrctn': 'ISRCTN31181395'}]
        conn['warehouse']['pubmed'].update(pubmed_attrs, ['pmid'])
        processor.process({}, conn)

        document = conn['database']['documents'].find_one(
            source_url=pubmed_attrs['meta_source']
        )
        assert document is None


    def test_deletes_unregistered_trial_record_if_registry_ids_added(self, conn,
        pubmed_record, record):

        conn['database']['records'].update(
            {
                'id': record,
                'identifiers': {'pubmed': ('PUBMED%s' % pubmed_record)},
            },
            ['id']
        )
        processor.process({}, conn)

        assert conn['database']['records'].find_one(id=record) is None


@pytest.fixture
def results_document_category(conn, document_category):
    extractors = helpers.get_variables(
        extractors_module, lambda x: x.startswith('extract_')
    )
    doc_category_id = extractors['extract_document_category'](None)
    doc_category_attrs = conn['database']['document_categories'].find_one(id=document_category)
    doc_category_attrs['id'] = doc_category_id
    conn['database']['document_categories'].update(doc_category_attrs, ['name', 'group'])
