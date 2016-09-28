# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import groupby

import time
import pbclient as pbc
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
        pbc.set('endpoint', conf['PYBOSSA_URL'])
        pbc.set('api_key', conf['PYBOSSA_API_KEY'])
        project_id = conf['PYBOSSA_PROJECT_INDICATIONS']

        _create_tasks(rows, project_id)
    else:
        logger.info('No new and modified indications found for tasks creation')


def _create_tasks(rows, project_id):
    tasks = []
    for key, group in groupby(rows, lambda x: x['fda_approval_id']):
        group = list(group)
        first = group[0]
        task = {
            'fda_approval_id': str(first['fda_approval_id'])
        }
        task['documents'] = [{'document_id': str(doc['document_id']), 'name': doc['name'], 'url': doc['url']}
                             for doc in group]
        tasks.append(task)

    logger.debug('{} tasks in the database'.format(len(tasks)))
    _submit_tasks(tasks, project_id)


def _submit_tasks(tasks, project_id):
    existing_ids = _get_existing_ids(project_id)
    cleaned_tasks = [t for t in tasks
                     if t['fda_approval_id'] not in existing_ids]

    logger.debug('{} tasks to be created'.format(len(cleaned_tasks)))

    for task in cleaned_tasks:
        _submit_task(task, project_id)


def _get_existing_ids(project_id):
    tasks = []
    limit = 100

    while True:
        last_id = tasks[-1].id if tasks else None
        response = pbc.get_tasks(project_id, limit=limit, last_id=last_id)

        if not response:
            break

        if not _wait_if_reached_rate_limit(response):
            tasks.extend(response)

    logger.debug('{} tasks on the server'.format(len(tasks)))
    return [task.info['fda_approval_id'] for task in tasks]


def _submit_task(task, project_id):
    res = pbc.create_task(project_id, task)
    if _wait_if_reached_rate_limit(res):
        _submit_task(task, project_id)


def _wait_if_reached_rate_limit(response):
    '''Sleeps and return True if we reached rate limit, otherwise return None.

    It'll throw an exception if the response's status code is different from
    429.
    '''
    try:
        if response.get('status_code') == 429:
            logger.debug('Rate limit reached, sleeping for 5 minutes')
            time.sleep(300)
        else:
            raise Exception('Received unexpected response', response)

        return True
    except AttributeError:
        pass
