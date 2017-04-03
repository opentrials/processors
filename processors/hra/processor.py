# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base
from . import extractors as extractors_module


def process(conf, conn):
    extractors = base.helpers.get_variables(
        extractors_module, lambda x: x.startswith('extract_')
    )
    base.processors.process_publications(conn, 'hra', extractors)
