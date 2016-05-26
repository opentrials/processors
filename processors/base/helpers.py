# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import json
import string
import datetime


# Module API

def get_variables(object, filter=None):
    """Exract variables from object to dict using name filter.
    """
    variables = {}
    for name, value in vars(object).items():
        if filter is not None:
            if not filter(name):
                continue
        variables[name] = value
    return variables


def slugify_string(string):
    """Slugify string
    """
    string = re.sub(r'[\W_]+', '_', string)
    string = string.strip('_')
    string = string.lower()
    return string


def slugify_array(array, min_length=5):
    """Slugify copy of array: slugify + uniquify + sort + remove short items
    """
    result = []
    for item in array:
        if item and len(item) > min_length:
            item = slugify_string(item)
            result.append(item)
    result = list(sorted(set(result)))
    return result


class JSONEncoder(json.JSONEncoder):
    """JSON encoder with datetime, date set support.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def clean_dict(raw_dict):
    """Remove falsy values from dict.
    """
    cleaned_dict = {}
    for key, value in raw_dict.items():
        if value:
            cleaned_dict[key] = value
    return cleaned_dict


def get_optimal_title(*titles):
    """Return first striped title with enough length or last striped title.
    """
    MIN_LENGTH = 10
    for title in titles:
        title = clean_string(title)
        if len(title) >= MIN_LENGTH:
            return title
    return title


def clean_string(value):
    """Cast falsy value to sring and strip whitespeces and other unwanted chars.
    """
    if not value:
        value = ''
    value = value.strip(string.whitespace + '.')
    return value
