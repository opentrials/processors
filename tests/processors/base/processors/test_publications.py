# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from processors.base import helpers
import processors.pubmed_publications.extractors as extractors_module
from processors.base.processors.publication import process_publications


class TestPublicationProcessor(object):
    def test_creates_publication(self, conn, extractors, pubmed_record):
        pubmed_attrs = conn['warehouse']['pubmed'].find_one(pmid=pubmed_record)
        process_publications(conn, 'pubmed', extractors)

        publication = conn['database']['publications'].find_one(
            source_url=pubmed_attrs['meta_source']
        )
        assert publication is not None


    def test_links_publication_to_trial(self, conn, extractors, pubmed_record, trial, record):
        identifier = {'nct': 'NCT00020500'}
        conn['warehouse']['pubmed'].update(
            {
                'pmid': pubmed_record,
                'article_title': 'This publication is related to %s' % identifier,
            },
            ['pmid']
        )
        conn['database']['records'].update(
            {
                'id': record,
                'trial_id': trial,
                'identifiers': identifier,
            },
            ['id']
        )
        process_publications(conn, 'pubmed', extractors)

        trials_publications = conn['database']['trials_publications'].find_one(
            trial_id=trial
        )
        assert trials_publications is not None


@pytest.fixture
def extractors():
    return helpers.get_variables(extractors_module,
        lambda x: x.startswith('extract_'))
