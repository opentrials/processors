# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Extractor(object):

    # Public

    @property
    @abstractmethod
    def basis(self):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def table(self):
        pass  # pragma: no cover

    @abstractmethod
    def extract(self, target, item=None):
        """Extract data from item.

        Args:
            target (str): target like `trial`
            item (dict): source item

        Returns:
            dict: extracted data

        """
        pass  # pragma: no cover
