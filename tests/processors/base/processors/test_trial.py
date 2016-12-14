# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid
from processors.base import helpers
import processors.nct.extractors as nct_extractors
from processors.base.processors.trial import process_trials


class TestTrialProcessor(object):
    def test_updates_which_record_is_primary(self, conn, extractors, trial, record,
        nct_record, euctr_source):

        current_primary = conn['database']['records'].find_one(id=record)
        nct_record_attrs = conn['warehouse']['nct'].find_one(nct_id=nct_record)
        current_primary.update({
            'trial_id': trial,
            'is_primary': True,
            'source_id': euctr_source,
            'identifiers': {'nct': nct_record},
        })
        conn['database']['records'].update(current_primary, ['id'])

        process_trials(conn, 'nct', extractors)
        updated_current_primary = conn['database']['records'].find_one(id=record)
        new_record = conn['database']['records'].find_one(id=nct_record_attrs['meta_id'])

        assert updated_current_primary['is_primary'] == False
        assert new_record['is_primary'] ==  True


@pytest.fixture
def extractors():
    return helpers.get_variables(nct_extractors,
        lambda x: x.startswith('extract_'))
