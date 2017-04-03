# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


def extract_document(record):
    return {
        'name': record['article_title'],
        'source_url': record['meta_source'],
    }


def extract_document_category(record):
    return base.config.DOCUMENT_CATEGORIES['journal_article']


def extract_trial(record):
    pubmed_id = base.helpers.safe_prepend('PUBMED', record['pmid'])
    identifiers = base.helpers.clean_identifiers({
        'pubmed': pubmed_id,
    })

    return {
        'public_title': record['article_title'],
        'scientific_title': record['article_title'],
        'brief_summary': record['article_abstract'],
        'identifiers': identifiers,
    }
