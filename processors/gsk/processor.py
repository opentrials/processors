# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base
from . import extractors


# Module API

def process(conn):
    base.processors.process_trial(conn, 'gsk', extractors)

