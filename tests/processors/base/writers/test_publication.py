# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.base.writers as writers


class TestPublicationWriter(object):
    def test_skips_publication_with_invalid_url(self):
        publication = {
            'slug': 'publication_slug',
            'source_url': 'url',
            'title': 'title',
            'abstract': 'abstract',
        }
        source_id = 'source_id'
        conn = _get_mock_conn()
        conn['database']['publications'].find_one.return_value = None

        assert writers.write_publication(conn, publication, source_id) is None

    def test_writes_publication_with_valid_url(self):
        publication = {
            'slug': 'publication_slug',
            'source_url': 'http://www.ncbi.nlm.nih.gov/pubmed/23622910',
            'title': 'title',
            'abstract': 'abstract',
        }
        source_id = 'source_id'
        conn = _get_mock_conn()
        conn['database']['publications'].find_one.return_value = None

        assert writers.write_publication(conn, publication, source_id) is not None


def _get_mock_conn():
    return {
        'database': {
            'publications': mock.Mock(),
        },
    }
