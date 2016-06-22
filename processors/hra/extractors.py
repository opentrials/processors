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
    }
    return source


def extract_publications(record):

    # Get title
    title = base.helpers.get_optimal_title(
        record['application_title'],
        record['application_full_title'],
        record['hra_id'])

    # Get abstract
    abstract = record['research_summary'] or title
    identifiers = base.helpers.clean_list({
        _clean_identifier(record['nct_id'], prefix='NCT'),
        _clean_identifier(record['euctr_id'], prefix='EUCTR'),
        _clean_identifier(record['isrctn_id'], prefix='ISRCTN'),
    })
    if identifiers:
        abstract = '%s [%s]' % (abstract, '/'.join(identifiers))

    # Get slug
    slug = base.helpers.slugify_string(
        '%s_%s' % (title, record['publication_date']))

    # Extract publications
    publications = []
    publications.append({
        'source_url': record['meta_source'],
        'title': title,
        'abstract': abstract,
        'date': record['publication_date'],
        # ---
        'slug': slug,
    })

    return publications


# Internal

def _clean_identifier(ident, prefix):
    if ident:
        ident = ident.strip()
        if re.match(r'%s\d{3,}' % prefix, ident):
            return ident
        if re.match(r'\d{3,}', ident):
            return '%s%s' % (prefix, ident)
    return None
