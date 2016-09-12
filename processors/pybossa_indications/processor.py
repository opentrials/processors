# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import groupby

import time
import requests
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
        GROUP BY fda_approvals.id,
                 documents.id,
                 files.id
        ORDER BY fda_approvals.id
    """

    rows = list(conn['database'].query(query))
    if rows:
        _create_tasks(conf, rows)
    else:
        logger.info('No new and modified indications found for tasks creation')


def _create_tasks(conf, rows):
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
    _submit_tasks(conf, tasks)


def _pybossa_rate_limitation(conf, endpoint):
    # This should be called before actual requests to avoid getting HTTP 429s
    res = requests.get('{}/api/{}'.format(conf['PYBOSSA_URL'], endpoint))
    if int(res.headers['X-RateLimit-Remaining']) < 10:
        logger.warn('Rate limit reached, will sleep for 5 minutes')
        time.sleep(300)  # Sleep for 5 minutes


def _get_existing_ids(conf, PYBOSSA_PROJECT_INDICATIONS):
    tasks = []
    limit = 100

    while True:
        # Make sure we have enough requests left
        _pybossa_rate_limitation(conf, 'task')
        last_id = tasks[-1].id if tasks else None
        collection = pbc.get_tasks(conf['PYBOSSA_PROJECT_INDICATIONS'], limit=limit, last_id=last_id)
        tasks.extend(collection)
        if not collection:
            break
    logger.debug('{} tasks on the server'.format(len(tasks)))
    return [task.info['fda_approval_id'] for task in tasks]


def _submit_tasks(conf, tasks):

    # Set up PyBossa connection
    pbc.set('endpoint', conf['PYBOSSA_URL'])
    pbc.set('api_key', conf['PYBOSSA_API_KEY'])

    # Get existing IDs
    existing_ids = _get_existing_ids(conf, conf['PYBOSSA_PROJECT_INDICATIONS'])
    if not existing_ids:
        logger.error('Cannot get the list of existing task IDs')

    cleaned_tasks = [t for t in tasks
                     if t['fda_approval_id'] not in existing_ids]

    logger.debug('{} tasks to be created'.format(len(cleaned_tasks)))

    for task in cleaned_tasks:
        _submit_task(conf, task)


def _submit_task(conf, task):
    res = pbc.create_task(conf['PYBOSSA_PROJECT_INDICATIONS'], task)
    if isinstance(res, dict) and res['status_code'] == 429:
        _pybossa_rate_limitation(conf, 'task')
        _submit_task(task, conf['PYBOSSA_PROJECT_INDICATIONS'])
