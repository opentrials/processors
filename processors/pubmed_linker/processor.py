# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Iterate over all pubmed publications
    count = 0
    for publication in base.helpers.iter_rows(conn, 'database', 'publications',
            orderby='id', source_id='pubmed'):
        try:

            # Find identifiers
            list_of_identifiers = base.helpers.find_list_of_identifiers(
                publication['title'] + publication['abstract'])

            # Delete existent relationships
            conn['database']['trials_publications'].delete(
                publication_id=publication['id'])

            # Write new relationships
            for identifiers in list_of_identifiers:

                # Get trial
                trial = base.helpers.find_trial_by_identifiers(
                    conn, identifiers=identifiers)

                # Found trial - add relationship
                if trial:
                    base.writers.write_trial_relationship(
                        conn, 'publication', publication, publication['id'], trial['id'])
                    logger.debug('Linked %s to "%s"',
                        trial['identifiers'].values(), publication['title'][0:50])

                # Not found trial - add trial stub
                else:
                    trial = {
                        'source_id': 'pubmed',
                        'identifiers': identifiers,
                        'public_title': identifiers.values()[0],
                    }
                    base.writers.write_trial(conn, trial, 'pubmed')
                    logger.debug('Added pubmed-only trial: %s', identifiers.values()[0])

            # Log info
            count += 1
            if not count % 100:
                logger.info('Processed for links %s pubmed publications', count)

        except Exception:
            base.config.SENTRY.captureException(extra={
                'publication': publication,
            })
