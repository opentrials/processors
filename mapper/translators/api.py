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

    def __init__(self, warehouse, database, extractor):
        pass  # pragma: no cover

    @property
    @abstractmethod
    def direct(self):
        pass  # pragma: no cover

    @abstractmethod
    def translate(self):
        pass  # pragma: no cover
