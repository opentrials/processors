# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
from .. import base


def extract_source(record):
    return {
        'id': 'hra',
        'name': 'Health Research Authority',
        'type': 'other',
        'source_url': 'http://www.hra.nhs.uk',
        'terms_and_conditions_url': 'http://www.hra.nhs.uk/terms-conditions/',
    }


def extract_publication(record):

    # Get title
    title = base.helpers.get_optimal_title(
        record['application_title'],
        record['application_full_title'],
        record['hra_id']
    )

    # Get URL for humans
    source_url = _url_from_title(record['application_title'])

    # Get abstract
    abstract = record['research_summary'] or title

    # Get identifiers
    registry_ids = base.helpers.clean_identifiers({
        'nct': base.helpers.safe_prepend('NCT', record['nct_id']),
        'euctr': base.helpers.safe_prepend('EUCTR', record['euctr_id']),
        'isrctn': base.helpers.safe_prepend('ISRCTN', record['isrctn_id']),
    })
    search_id_fields = [title, abstract]
    identifiers = base.helpers.find_list_of_identifiers(' '.join(search_id_fields))
    if registry_ids:
        identifiers.append(registry_ids)

    # Get slug
    slug = base.helpers.slugify_string(
        '%s_%s' % (title, record['publication_date'])
    )

    # Extract publications
    return {
        'source_url': source_url,
        'title': title,
        'abstract': abstract,
        'date': record['publication_date'],
        # ---
        'slug': slug,
        'identifiers': identifiers,
    }


def _url_from_title(title):
    """Creates an HRA URL from an application title
    """
    slug = re.sub(r'[/]+', '', title)
    slug = re.sub(r'[\W_]+', '-', slug)
    slug = slug.strip('-')
    slug = slug.lower()
    url = 'http://www.hra.nhs.uk/news/research-summaries/' + slug
    return url
