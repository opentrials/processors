# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


def extract_source(record):
    return {
        'id': 'pubmed',
        'name': 'PubMed',
        'type': 'other',
        'source_url': 'http://www.ncbi.nlm.nih.gov/pubmed',
        'terms_and_conditions_url': 'https://www.ncbi.nlm.nih.gov/home/about/policies.shtml',
    }


def extract_publication(record):
    # Get article abstract
    article_abstract = record['article_title']
    if record['article_abstract']:
        article_abstract = record['article_abstract']

    # Get identifiers
    raw_registry_ids = record['registry_ids'] or []
    registry_ids = []
    for ids in raw_registry_ids:
        for id_name, id_value in ids.items():
            id_value = _clean_identifier(id_name, id_value)
            normalized_ids = base.helpers.find_list_of_identifiers(id_value)
            registry_ids.extend(normalized_ids)

    pubmed_id = base.helpers.safe_prepend('PUBMED', record['pmid'])
    search_id_fields = [article_abstract, record['article_title'], pubmed_id]
    identifiers = base.helpers.find_list_of_identifiers(' '.join(search_id_fields))
    identifiers.extend(registry_ids)

    # Get slug
    slug = base.helpers.slugify_string(
        '%s_%s' % (record['article_title'], record['date_created'])
    )

    # Extract publications
    return {
        'source_url': record['meta_source'],
        'title': record['article_title'],
        'abstract': article_abstract,
        'authors': record['article_authors'],
        'journal': record['journal_title'],
        'date': record['article_date'],
        # ---
        'slug': slug,
        'registry_ids': registry_ids,
        'identifiers': identifiers,
    }


def _clean_identifier(pubmed_name, identifier):
    if pubmed_name.lower() == 'eudract':
        identifier = base.helpers.safe_prepend('EUCTR', identifier)
    return identifier
