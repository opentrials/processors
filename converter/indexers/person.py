# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
from datetime import datetime

from .. import base
logger = logging.getLogger(__name__)


class PersonIndexer(base.Indexer):

    # Public

    table = 'index_persons'

    def index(self):
        pass
