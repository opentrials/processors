# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import mock
import datetime
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

    @mock.patch('processors.fda_dap.processor.FDADAPProcessor._find_intervention')
    def test_process_record(self, find_intervention_mock):
        find_intervention_mock.return_value = None
        conf = {}
        conn = {}
        document = {
            'fda_application_num': 'NDA000000',
        }
        proc = processor.FDADAPProcessor(conf, conn)
        result = proc.process_record(document, 'source_id')

        assert result is None
