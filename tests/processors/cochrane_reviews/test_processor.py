# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import processors.cochrane_reviews.processor as processor


class TestCochraneProcessor(object):
    def test_get_ref_identifiers(self):
        reference = {
            'layingaround': 'NCT    87654321',
            'identifiers': [
                {'type': 'OTHER', 'value': 'PMID should not be matched 1860386'},
                {'type': 'PUBMED', 'value': '12345678'},
            ]
        }
        identifiers = processor.extract_ref_identifiers(reference)
        expected = {
            'pubmed_id': '12345678',
            'nct_id': '87654321',
        }
        assert identifiers == expected

    def test_scrape_pubmed_id(self):
        reference = {
            'year': '2007',
            'title': ('Rivastigmine treatment as an add-on to antipsychotics in '
                      'patients with schizophrenia and cognitive deficit'),
            'authors': ('Chouinard S, Stip E, Poulin J, Melun JP, '
                        'Godbout R, Guillem F, Cohen H')
        }
        pmid = processor.scrape_pubmed_id(reference)

        assert pmid == '17355738'
