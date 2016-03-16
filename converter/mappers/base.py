# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Mapper(object):

    # Public

    def __init__(self, warehouse, database):
        self.__warehouse = warehouse
        self.__database = database

    @property
    def warehouse(self):
        """object: Warehouse dataset connection.
        """
        return self.__warehouse

    @property
    def database(self):
        """object: Database dataset connection.
        """
        return self.__database

    @abstractmethod
    def map(self):
        """Map data.
        """
        pass  # pragma: no cache
