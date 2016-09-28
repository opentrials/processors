# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import pbclient
import processors.base.helpers as helpers


class TestPyBossaTasksUpdater(object):
    def test_it_configures_pbclient(self):
        endpoint = 'http://example.org'
        api_key = 'API_KEY'
        project_id = None

        helpers.PyBossaTasksUpdater(endpoint, api_key, project_id)

        assert pbclient._opts['endpoint'] == endpoint
        assert pbclient._opts['api_key'] == api_key

    @mock.patch('processors.base.helpers.pybossa_tasks_updater.pbclient')
    def test_it_creates_tasks(self, pbclient_mock):
        endpoint = 'http://example.org'
        api_key = 'API_KEY'
        project_id = None
        tasks_data = [
            {'foo': 50},
        ]
        existing_tasks = []

        _setup_pbclient_mock(pbclient_mock)

        updater = helpers.PyBossaTasksUpdater(endpoint, api_key, project_id)
        updater.run(tasks_data, ['foo'])

        pbclient_mock.create_task.assert_called_with(project_id, tasks_data[0])

    @mock.patch('processors.base.helpers.pybossa_tasks_updater.pbclient')
    def test_it_doesnt_create_new_tasks_if_they_already_exist(self, pbclient_mock):
        endpoint = 'http://example.org'
        api_key = 'API_KEY'
        project_id = None
        tasks_data = [
            {'foo': 50},
        ]
        existing_tasks = [_mock_task(data) for data in tasks_data]

        _setup_pbclient_mock(pbclient_mock, existing_tasks)

        updater = helpers.PyBossaTasksUpdater(endpoint, api_key, project_id)
        updater.run(tasks_data, ['foo'])

        pbclient_mock.create_task.assert_not_called()

    @mock.patch('processors.base.helpers.pybossa_tasks_updater.pbclient')
    def test_it_deletes_tasks_that_dont_exist_in_the_received_tasks_data(self, pbclient_mock):
        endpoint = 'http://example.org'
        api_key = 'API_KEY'
        project_id = None
        tasks_data = []
        existing_tasks = [
            _mock_task({'foo': 50}),
        ]

        _setup_pbclient_mock(pbclient_mock)

        pbclient_mock.get_tasks.side_effect = [existing_tasks, None]

        updater = helpers.PyBossaTasksUpdater(endpoint, api_key, project_id)
        updater.run(tasks_data, ['foo'])

        pbclient_mock.delete_task.assert_called_with(existing_tasks[0].id)

    @mock.patch('processors.base.helpers.pybossa_tasks_updater.pbclient')
    def test_it_updates_existing_tasks_with_new_data(self, pbclient_mock):
        endpoint = 'http://example.org'
        api_key = 'API_KEY'
        project_id = None
        tasks_data = [
            {'foo': 50, 'bar': 20},
        ]
        existing_tasks = [
            _mock_task({'foo': 50}),
        ]

        _setup_pbclient_mock(pbclient_mock)

        pbclient_mock.get_tasks.side_effect = [existing_tasks, None]

        updater = helpers.PyBossaTasksUpdater(endpoint, api_key, project_id)
        updater.run(tasks_data, ['foo'])

        assert existing_tasks[0].data['info'] == tasks_data[0]
        pbclient_mock.update_task.assert_called_with(existing_tasks[0])


def _mock_task(info):
    task = mock.Mock()
    task.id = 51
    task.data = {
        'info': info,
    }
    return task


def _setup_pbclient_mock(pbclient_mock, existing_tasks=None):
    pbclient_mock.create_task.return_value = None
    pbclient_mock.delete_task.return_value = None
    pbclient_mock.update_task.return_value = None

    if existing_tasks:
        pbclient_mock.get_tasks.side_effect = [existing_tasks, None]
    else:
        pbclient_mock.get_tasks.return_value = None
