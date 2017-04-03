# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import collections
import processors.hra.extractors as extractors


class TestHRAPublicationExtractor(object):
    def test_extracts_publication_identifiers(self):
        record = collections.defaultdict(lambda: '')
        record.update({
            'nct_id': '00020500',
            'euctr_id': '2013-030180-02',
            'isrctn_id': '02018090',
        })
        expected_identifiers = [{
            'nct': 'NCT00020500',
            'euctr': 'EUCTR2013-030180-02',
            'isrctn': 'ISRCTN02018090',
        }]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers


    def test_ignores_invalid_identifiers(self):
        record = collections.defaultdict(lambda: '')
        record.update({
            'nct_id': '00020500',
            'euctr_id': 'EUCTR0000-000000-00',
            'isrctn_id': 'ISRCTN00000000',
        })
        expected_identifiers = [{'nct': 'NCT00020500'}]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers


    def test_extracts_identifiers_from_abstract(self):
        record = collections.defaultdict(lambda: '')
        record['research_summary'] = 'This publication mentions NCT00020500'
        expected_identifiers = [{'nct': 'NCT00020500'}]
        publication = extractors.extract_publication(record)

        assert publication['identifiers'] == expected_identifiers


    def test_creates_url_from_title(self):
        record = collections.defaultdict(lambda: '')
        record['application_title'] = 'Longterm F/U study of BOTOX® in Idiopathic Overactive Bladder patients'
        expected_url = 'http://www.hra.nhs.uk/news/research-summaries/longterm-fu-study-of-botox-in-idiopathic-overactive-bladder-patients'
        publication = extractors.extract_publication(record)

        assert publication['source_url'] == expected_url
