# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from . import translators
logger = logging.getLogger(__name__)


# Module API

class Mapper(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    def map(self, translator, extractor):
        translator = getattr(translators, translator.capitalize())(
            self.__warehouse, self.__database, extractor)
        translator.convert()
