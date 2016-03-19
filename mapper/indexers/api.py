# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Indexer(object):
    """Trial indexer.

    Args:
        warehouse (object): dataset connection

    """

    # Public

    @abstractmethod
    def __init__(self, warehouse):
        pass  # pragma: no cache

    @property
    @abstractmethod
    def warehouse(self):
        """object: Warehouse dataset connection.
        """
        pass  # pragma: no cache

    @abstractmethod
    def index(self, **kwargs):
        """Index item (if not already exists) and return id.

        Args:
            kwargs (dict): item parameters required for indexing

        Returns:
            str: identifier

        """
        pass  # pragma: no cache
