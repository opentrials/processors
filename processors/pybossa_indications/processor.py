# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import groupby

import processors.base.helpers as helpers
import logging
logger = logging.getLogger(__name__)


def process(conf, conn):
    # Get FDA documents with type "New or Modified Indication"
    query = """
        SELECT documents.id AS document_id,
               fda_approvals.id AS fda_approval_id,
               documents.name,
               files.url
        FROM documents
        INNER JOIN fda_approvals ON documents.fda_approval_id = fda_approvals.id
        INNER JOIN files ON documents.file_id = files.id
        WHERE files.url IS NOT NULL
              AND fda_approvals.type = 'New or Modified Indication'
        ORDER BY fda_approvals.id
    """

    rows = list(conn['database'].query(query))
    if rows:
        # Set up PyBossa connection
        url = conf['PYBOSSA_URL']
        api_key = conf['PYBOSSA_API_KEY']
        project_id = conf['PYBOSSA_PROJECT_INDICATIONS']
        processor = helpers.PyBossaTasksUpdater(url, api_key, project_id)

        tasks_data = _create_tasks(rows)

        processor.run(tasks_data, ['fda_approval_id'])
    else:
        logger.info('No new and modified indications found for tasks creation')


def _create_tasks(rows):
    tasks = []
    for key, group in groupby(rows, lambda x: x['fda_approval_id']):
        group = list(group)
        first = group[0]
        task = {
            'fda_approval_id': str(first['fda_approval_id']),
            'documents': [_extract_document(doc) for doc in group],
        }
        tasks.append(task)

    logger.debug('{} tasks in the database'.format(len(tasks)))

    return tasks


def _extract_document(document):
    return {
        'document_id': str(document['document_id']),
        'name': document['name'],
        'url': document['url'],
    }
