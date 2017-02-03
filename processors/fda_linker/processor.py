# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import base
logger = logging.getLogger(__name__)


def process(conf, conn):
    count = 0
    for document in base.helpers.iter_rows(conn, 'database', 'documents',
                                           orderby='id', source_id='fda'):
        try:
            document_file = conn['database']['files'].find_one(id=document['file_id'])
            document_log_name = document['fda_approval_id'] + ' ' + document['name']

            if not document_file:
                continue

            # Find identifiers
            list_of_identifiers = []
            for page in document_file['pages'] or []:
                list_of_identifiers.extend(base.helpers.find_list_of_identifiers(page))

            # Delete existent relationships
            conn['database']['trials_documents'].delete(document_id=document['id'])

            # Write new relationships
            for identifiers in select_unique_identifiers(list_of_identifiers):

                # Get trial
                trial = base.helpers.find_trial_by_identifiers(
                    conn, identifiers=identifiers)

                if trial:
                    base.writers.write_trial_relationship(
                        conn, 'document', document, document['id'], trial['id'])
                    logger.debug('Linked %s to "%s"',
                        trial['identifiers'].values(), document_log_name)
                    count += 1
                else:
                    logger.debug('Attempt to link FDA document "%s" failed. No trial found with identifiers %s',
                        document_log_name, identifiers)
        except Exception:
            base.config.SENTRY.captureException(extra={
                'document': document,
            })

    logger.info('Linked %s FDA documents to trials', count)


def select_unique_identifiers(list_of_identifiers):
    """Select only unique identifiers from list of identifiers"""

    unique_identifiers = [dict(pair) for pair in set(frozenset(identifier.items())
                          for identifier in list_of_identifiers)]

    return unique_identifiers
