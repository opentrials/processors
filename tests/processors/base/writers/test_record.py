# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import processors.base.writers as writers


class TestRecordWriter(object):
    def test_skips_record_with_invalid_url(self, conn, trial, nct_source):
        record = {
            'meta_id': uuid.uuid1().hex,
            'meta_created': '2016-05-26 05:42:33.555790 +03:00',
            'meta_updated': '2016-05-26 05:42:33.555790 +03:00',
            'meta_source': 'url',
        }
        trial_record = conn['database']['trials'].find_one(id=trial)

        assert writers.write_record(conn, record, nct_source, trial, trial_record) is None


    def test_writes_record_with_valid_url(self, conn, trial, nct_source):
        record = {
            'meta_id': uuid.uuid1().hex,
            'meta_created': '2016-05-26 05:42:33.555790 +03:00',
            'meta_updated': '2016-05-26 05:42:33.555790 +03:00',
            'meta_source': 'http://www.pfizer.com/research/clinical_trials/find_a_trial/NCT00666575',
        }
        trial_record = conn['database']['trials'].find_one(id=trial)

        assert writers.write_record(conn, record, nct_source, trial, trial_record) is not None
