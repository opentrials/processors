# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import processors.fda_dap.processor as processor


class TestFDADAPProcessor(object):
    @mock.patch('processors.base.writers.write_source')
    def test_create_source(self, write_mock):
        expected_source = {
            'id': 'fda',
            'name': 'U.S. Food and Drug Administration',
            'type': 'other',
        }
        conn = {}
        processor._create_source(conn)

        write_mock.assert_called_with(conn, expected_source)
