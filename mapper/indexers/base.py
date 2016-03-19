# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod

from . import api


# Module API

@add_metaclass(ABCMeta)
class Indexer(api.Indexer):

    # Public

    def __init__(self, warehouse):
        self.__warehouse = warehouse

    @property
    def warehouse(self):
        return self.__warehouse
