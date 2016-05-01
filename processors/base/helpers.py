# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import json
import datetime


# Module API

def slugify_array(array, min_length=5):
    """Slugify copy of array: slugify + uniquify + remove short items
    """
    result = []
    for item in array:
        if item and len(item) > min_length:
            item = re.sub(r'[\s_]+', '_', item)
            item = re.sub(r'\W', '', item)
            item = item.lower()
            result.append(item)
    result = list(set(result))
    return result


class JSONEncoder(json.JSONEncoder):
    """JSON encoder with datetime, date set support.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime ('%Y-%m-%d')
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
