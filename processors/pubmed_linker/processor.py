# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Iterate over all pubmed publications
    count = 0
    for publication in base.readers.read_rows(conn, 'database', 'publications',
            orderby='id', source_id='pubmed'):

        # Find identifiers
        identifiers = _find_identifiers(
            publication['title'] + publication['abstract'])

        # Delete existent relationships
        conn['database']['trials_publications'].delete(
            publication_id=publication['id'])

        # Write new relationships
        for identifier in identifiers:

            # Get trial
            trial_facts = base.helpers.slugify_array([identifier])
            trial = base.readers.read_objects(
                conn, 'trials', first=True, facts=trial_facts)

            # Found trial - add relationship
            if trial:
                base.writers.write_trial_relationship(
                    conn, 'publication', publication, publication['id'], trial['id'])
                logger.debug('Linked %s to "%s"',
                    trial['primary_id'], publication['title'][0:50])

            # Not found trial - add trial stub
            else:
                trial = {
                    'primary_register': 'Pubmed',
                    'primary_id': identifier,
                    'identifiers': {
                        'pubmed': identifier,
                    },
                    'public_title': identifier,
                }
                base.writers.write_trial(conn, trial, 'pubmed')
                logger.debug('Added pubmed-only trial: %s', identifier)

        # Log info
        count += 1
        if not count % 100:
            logger.info('Processed for links %s pubmed publications', count)


# Internal

def _find_identifiers(text):
    # Pattern could be improved based on a extended
    # clinical trial identifiers format analysis
    PATTERN = r'(%s\d{3,})'
    PREFIXES = [
        'actrn',
        'euctr',
        'gsk',
        'isrctn',
        'jprn',
        'nct',
        'takeda',
        'umin',
    ]

    # Find identifiers
    identifiers = []
    for prefix in PREFIXES:
        pattern = PATTERN % prefix
        identifiers.extend(re.findall(pattern, text, re.IGNORECASE))

    return identifiers
