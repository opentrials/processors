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

    # Find identifiers
    identifiers = _find_identifiers(
        record['article_title'] + record['article_abstract'])

    # Extract publications
    publications = []
    publications.append({
        'source_url': record['meta_source'],
        'title': record['article_title'],
        'abstract': record['article_abstract'],
        'authors': record['article_authors'],
        'journal': record['journal_title'],
        'date': record['article_date'],
        # ---
        'trial_identifiers': identifiers,
    })

    return publications


# Internal

def _find_identifiers(text):
    # Pattern could be improved based on a extended
    # clinical trial identifiers format analysis
    PATTERN = r'(%s\d{3,})'
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

    # Find identifiers
    identifiers = []
    for prefix in PREFIXES:
        pattern = PATTERN % prefix
        identifiers.extend(re.findall(pattern, text))

    return identifiers
