# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from six import add_metaclass
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


# Module API

@add_metaclass(ABCMeta)
class Translator(object):

    # Public

    @abstractmethod
    def translate(self):
        """Transate something from source to target.
        """
        pass  # pragma: no cover
