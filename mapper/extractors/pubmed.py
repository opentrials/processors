# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import logging

from . import base
logger = logging.getLogger(__name__)


# Module API

class PubmedExtractor(base.Extractor):

    # Public

    store = 'warehouse'
    table = 'pubmed'
    heads = []

    def extract_source(self, item):

        # Extract
        source = {
            'name': 'pubmed',
            'type': 'other',
        }

        return source

    def extract_publication(self, item):

        # Extract identifiers
        # TODO: find other identifiers
        pattern = r'((?:NCT\d{3,})|(?:ISRCTN\d{3,}))'
        contents = item['article_title'] + item['article_abstract']
        identifiers = re.findall(pattern, contents)

        # Extract publication
        publication = {
            'identifiers': identifiers,
            'source_url': item['meta_source'],
            'title': item['article_title'],
            'abstract': item['article_abstract'],
            'authors': item.get('article_authors', None),
            'journal': item.get('journal_title', None),
            'date': item.get('article_date', None),
        }

        return publication
