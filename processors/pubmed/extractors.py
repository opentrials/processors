# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re


# Module API

def extract_source(record):
    source = {
        'id': 'pubmed',
        'name': 'Pubmed',
        'type': 'other',
    }
    return source


def extract_publications(record):

    # Id prefixes
    PREFIXES = [
        'ACTRN',
        'EUCTR',
        'GSK',
        'ISRCTN',
        'JPRN',
        'NCT',
        'TAKEDA',
        'UMIN',
    ]

    # Extract identifiers
    pattern = r'({prefix}\d{3,})'
    contents = record['article_title'] + record['article_abstract']
    identifiers = []
    for prefix in PREFIXES:
        identifiers.append(
            re.findall(pattern.format(prefix=prefix), contents))

    # Extract publications
    publications = []
    publications.append({
        'source_url': record['meta_source'],
        'title': record['article_title'],
        'abstract': record['article_abstract'],
        'authors': record.get('article_authors', None),
        'journal': record.get('journal_title', None),
        'date': record.get('article_date', None),
        # ---
        'trial_identifiers': identifiers,
    })

    return publications
