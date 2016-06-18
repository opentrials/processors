# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# Module API

def extract_source(record):
    source = {
        'id': 'pubmed',
        'name': 'Pubmed',
        'type': 'other',
    }
    return source


def extract_publications(record):

    # Get article abstract
    article_abstract = record['article_title']
    if record['article_abstract']:
        article_abstract = record['article_abstract']

    # Extract publications
    publications = []
    publications.append({
        'source_url': record['meta_source'],
        'title': record['article_title'],
        'abstract': article_abstract,
        'authors': record['article_authors'],
        'journal': record['journal_title'],
        'date': record['article_date'],
    })

    return publications
