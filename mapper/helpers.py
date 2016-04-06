# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import json
import hashlib
import datetime


# Module API

def slugify(string, hash=False):
    slug = None
    if string:
        slug = re.sub(r'\W', '', string).lower() or None
    if slug and hash:
        slug = hashlib.md5(slug).hexdigest()
    return slug


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime ('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)
