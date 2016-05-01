# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re


# Module API

def extract_source(record):
    source = {
        'name': 'pubmed',
        'type': 'other',
        'data': {},
    }
    return source


def extract_publication(record):

    # Extract identifiers
    # TODO: find other identifiers
    pattern = r'((?:NCT\d{3,})|(?:ISRCTN\d{3,}))'
    contents = record['article_title'] + record['article_abstract']
    identifiers = re.findall(pattern, contents)

    # Extract publication
    publication = {
        'identifiers': identifiers,
        'source_url': record['meta_source'],
        'title': record['article_title'],
        'abstract': record['article_abstract'],
        'authors': record.get('article_authors', None),
        'journal': record.get('journal_title', None),
        'date': record.get('article_date', None),
    }

    return publication
