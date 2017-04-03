# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import collections
import processors.pubmed_publications.extractors as extractors


class TestPubmedPublicationsExtractor(object):
    def test_extracts_registry_identifiers(self):
        record = collections.defaultdict(lambda: '')
        record['registry_ids'] = [{"ClinicalTrials.gov": "NCT01572025"}]
        expected_identifiers = [{'nct': 'NCT01572025'}]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers


    def test_includes_pubmed_id_in_identifiers(self):
        record = collections.defaultdict(lambda: '')
        record['pmid'] = '24433108'
        expected_identifiers = [{'pubmed': 'PUBMED24433108'}]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers


    def test_extracts_identifiers_from_abstract(self):
        record = collections.defaultdict(lambda: '')
        record['article_abstract'] = 'This publication mentions NCT01572025'
        expected_identifiers = [{'nct': 'NCT01572025'}]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers
