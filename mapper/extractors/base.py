# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import add_metaclass
from abc import ABCMeta

from . import api


# Module API

@add_metaclass(ABCMeta)
class Extractor(api.Extractor):

    # Public

    def extract(self, target, item):

        # Get method
        try:
            method = getattr(self, 'extract_%s' % target)
        except AttributeError:
            message = 'Extractor %s doesn\'t support %s target.'
            message = message % (self, target)
            raise ValueError(message)

        # Extract data
        data = method(item)

        return data
