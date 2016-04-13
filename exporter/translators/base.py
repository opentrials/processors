# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta, abstractmethod


# Module API

@add_metaclass(ABCMeta)
class Translator(object):

    # Public

    @abstractmethod
    def __init__(self, warehouse, database):
        pass  # pragma: no cover

    @abstractmethod
    def translate(self):
        """Transate something from source to target.
        """
        pass  # pragma: no cover
