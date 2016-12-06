# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import processors.base.writers as writers


class TestPublicationWriter(object):
    def test_skips_publication_with_invalid_url(self, conn, nct_source):
        publication = {
            'slug': 'publication_slug',
            'source_url': 'url',
            'title': 'title',
            'abstract': 'abstract',
        }

        assert writers.write_publication(conn, publication, nct_source) is None


    def test_writes_publication_with_valid_url(self, conn, nct_source):
        publication = {
            'slug': 'publication_slug',
            'source_url': 'http://www.ncbi.nlm.nih.gov/pubmed/23622910',
            'title': 'title',
            'abstract': 'abstract',
        }

        assert writers.write_publication(conn, publication, nct_source) is not None
