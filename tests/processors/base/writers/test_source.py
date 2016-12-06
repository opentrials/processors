# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import processors.base.writers as writers


class TestSourceWriter(object):
    def test_skips_source_with_invalid_url(self, conn):
        source = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'source_url': 'invalid_url',
            'terms_and_conditions_url': 'http://example.org',
        }

        assert writers.write_source(conn, source) is None


    def test_skips_source_with_invalid_terms_and_conditions_url(self, conn):
        source = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'source_url': 'http://example.org',
            'terms_and_conditions_url': 'invalid_url',
        }

        assert writers.write_source(conn, source) is None


    def test_writes_source_with_valid_source_url_and_terms_and_conditions_url(self, conn):
        source = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
            'source_url': 'https://clinicaltrials.gov',
            'terms_and_conditions_url': 'https://clinicaltrials.gov/ct2/about-site/terms-conditions',
        }

        assert writers.write_source(conn, source) is not None


    def test_writes_source_without_urls(self, conn):
        source = {
            'id': 'id',
            'name': 'name',
            'type': 'type',
        }

        assert writers.write_source(conn, source) is not None
