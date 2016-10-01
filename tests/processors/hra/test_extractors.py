# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import collections
import processors.hra.extractors as extractors


class TestExtractPublications(object):
    def test_adds_identifiers_to_end_of_abstract(self):
        record = collections.defaultdict(lambda: '')
        record.update({
            'nct_id': '00020500',
            'euctr_id': '2013-030180-02',
            'isrctn_id': '02018090',
        })

        publication = extractors.extract_publications(record)[0]

        identifiers = '[EUCTR2013-030180-02/ISRCTN02018090/NCT00020500]'
        assert publication['abstract'].endswith(identifiers)

    def test_does_not_add_invalid_identifiers_to_abstract(self):
        record = collections.defaultdict(lambda: '')
        record.update({
            'nct_id': '00020500',
            'euctr_id': 'EUCTR0000-000000-00',
            'isrctn_id': 'ISRCTN00000000',
        })

        publication = extractors.extract_publications(record)[0]

        assert publication['abstract'].endswith('[NCT00020500]')
