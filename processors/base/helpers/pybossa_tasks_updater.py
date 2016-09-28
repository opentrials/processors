# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time
import pbclient
logger = logging.getLogger(__name__)


class PyBossaTasksUpdater(object):
    def __init__(self, endpoint, api_key, project_id):
        pbclient.set('endpoint', endpoint)
        pbclient.set('api_key', api_key)
        self.project_id = project_id

    def run(self, tasks_data, unique_keys):
        add, delete, update = self._filter_tasks(tasks_data, unique_keys)

        msg = '{} tasks to add, {} tasks to delete, {} tasks to update'
        logger.debug(msg.format(len(add), len(delete), len(update)))

        for task_data in add:
            self._add_task(task_data)

        for task in delete:
            self._delete_task(task)

        for task in update:
            self._update_task(task)

    def _filter_tasks(self, tasks_data, unique_keys):
        get_key = lambda value: tuple((key, value[key]) for key in unique_keys) # noqa: E731
        get_keys = lambda values: [get_key(value) for value in values] # noqa: E731

        existing_tasks = self._get_existing_tasks()
        existing_tasks_info = [task.data['info'] for task in existing_tasks]
        existing_ids = get_keys(existing_tasks_info)
        new_ids = get_keys(tasks_data)

        tasks_to_add = [task_data for task_data in tasks_data
                        if get_key(task_data) not in existing_ids]
        tasks_to_delete = [existing_tasks[i]
                           for i, task_info in enumerate(existing_tasks_info)
                           if get_key(task_info) not in new_ids]

        tasks_to_update = []
        for existing_task in existing_tasks:
            if existing_task in tasks_to_delete:
                continue
            try:
                index = new_ids.index(get_key(existing_task.data['info']))
            except ValueError:
                continue

            task_data = tasks_data[index]
            if task_data != existing_task.data['info']:
                existing_task.data['info'] = task_data
                tasks_to_update.append(existing_task)

        return tasks_to_add, tasks_to_delete, tasks_to_update

    def _get_existing_tasks(self):
        project_id = self.project_id
        tasks = []
        limit = 100

        while True:
            last_id = tasks[-1].id if tasks else None
            response = pbclient.get_tasks(project_id, limit=limit, last_id=last_id)

            if not response:
                break

            if not self._wait_if_reached_rate_limit(response):
                tasks.extend(response)

        logger.debug('{} tasks on the server'.format(len(tasks)))
        return tasks

    def _add_task(self, task_data):
        res = pbclient.create_task(self.project_id, task_data)
        if self._wait_if_reached_rate_limit(res):
            self._add_task(task_data)

    def _delete_task(self, task):
        res = pbclient.delete_task(task.id)
        if self._wait_if_reached_rate_limit(res):
            self._delete_task(task.id)

    def _update_task(self, task):
        res = pbclient.update_task(task)
        if self._wait_if_reached_rate_limit(res):
            self._update_task(task)

    def _wait_if_reached_rate_limit(self, response):
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
