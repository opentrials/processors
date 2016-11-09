# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import processors.fda_linker.processor as processor


class TestFDALinkerProcessor(object):
    @pytest.mark.parametrize('list_of_identifiers,unique_identifiers', [
        ([{'nct': 'NCT00020500'}, {'nct': 'NCT00020500'}], [{'nct': 'NCT00020500'}]),
        ([], []),
    ])
    def test_select_unique_identifiers(self, list_of_identifiers, unique_identifiers):
        assert processor.select_unique_identifiers(list_of_identifiers) == unique_identifiers
