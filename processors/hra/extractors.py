# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import base


# Module API


def extract_source(record):
    source = {
        'id': 'hra',
        'name': 'Health Research Authority',
        'type': 'other',
        'url': 'http://www.hra.nhs.uk',
        'terms_and_conditions_url': 'http://www.hra.nhs.uk/terms-conditions/',
    }
    return source


def extract_publications(record):

    # Get title
    title = base.helpers.get_optimal_title(
        record['application_title'],
        record['application_full_title'],
        record['hra_id'])

    # Get URL for humans
    source_url = _url_from_title(record['application_title'])

    # Get abstract
    abstract = record['research_summary'] or title
    identifiers = base.helpers.clean_identifiers({
        'nct': _clean_identifier(record['nct_id'], prefix='NCT'),
        'euctr': _clean_identifier(record['euctr_id'], prefix='EUCTR'),
        'isrctn': _clean_identifier(record['isrctn_id'], prefix='ISRCTN'),
    })
    if identifiers:
        abstract += ' [%s]' % ('/'.join(sorted(identifiers.values())))

    # Get slug
    slug = base.helpers.slugify_string(
        '%s_%s' % (title, record['publication_date']))

    # Extract publications
    publications = []
    publications.append({
        'source_url': source_url,
        'title': title,
        'abstract': abstract,
        'date': record['publication_date'],
        # ---
        'slug': slug,
    })

    return publications


# Internal

def _url_from_title(title):
    """Creates an HRA URL from an application title
    """
    slug = re.sub(r'[/]+', '', title)
    slug = re.sub(r'[\W_]+', '-', slug)
    slug = slug.strip('-')
    slug = slug.lower()
    url = 'http://www.hra.nhs.uk/news/research-summaries/' + slug
    return url


def _clean_identifier(ident, prefix):
    if ident:
        ident = ident.strip()
        if re.match(r'%s\d{3,}' % prefix, ident):
            return ident
        if re.match(r'\d{3,}', ident):
            return '%s%s' % (prefix, ident)
