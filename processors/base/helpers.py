# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import json
import uuid
import string
import logging
import datetime
logger = logging.getLogger(__name__)


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


def clean_list(raw_list):
    """Remove falsy values from list.
    """
    cleaned_list = []
    for value in raw_list:
        if value:
            cleaned_list.append(value)
    return cleaned_list


def get_cleaned_identifiers(identifiers):
    """Remove falsy values and bad identifiers.
    """
    PATTERNS = {
        'actrn': r'^ACTRN\d{14}p?',
        'chictr': r'^ChiCTR',
        'drks': r'^DRKS',
        'euctr': r'^EUCTR\d{4}-\d{6}-\d{2}',
        'gsk': r'^GSK',
        'irct': r'^IRCT',
        'isrctn': r'^ISRCTN\d{8}',
        'jprn': r'^JPRN-(C\d{9}|JapicCTI-\d{6}|JMA-IIA\d{5}|UMIN\d{9})',
        'kct': r'^KCT',
        'nct': r'^NCT\d{8}',
        'ntr': r'^NTR',
        'pactr': r'^PACTR',
        'per': r'^PER',
        'rbr': r'^RBR',
        'rpcec': r'^RPCEC',
        'takeda': r'^TAKEDA',
        'tctr': r'^TCTR',
        'who': r'^U\d{4}-\d{4}-\d{4}',
    }
    result = {}
    for key, value in identifiers.items():
        if not value:
            continue
        if key not in PATTERNS or not re.match(PATTERNS[key], value):
            message = 'Identifier "%s:%s" is not recognized'
            logger.warning(message, key, value)
            continue
        result[key] = value
    return result


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
    value = value.strip(string.whitespace + '."')
    return value


def find_list_of_identifiers(text):
    """Find list of trial indentifier dicts in the given text.

    Example:
        [{'nct': 'NCT123345'}, {'euctr': 'EUCTR12345'}]

    """

    # Pattern could be improved based on a extended
    # clinical trial identifiers format analysis
    PATTERN = r'(%s[\d-]{3,})'
    # In a form (source_id, pattern[])
    PREFIXES = [
        ('actrn', ['actrn']),
        ('euctr', ['euctr']),
        ('gsk', ['gsk']),
        ('isrctn', ['isrctn']),
        ('jprn', ['jprn', 'umin']),
        ('nct', ['nct']),
        ('takeda', ['takeda']),
    ]

    # Find identifiers
    list_of_identifiers = []
    for source_id, patterns in PREFIXES:
        for prefix in patterns:
            pattern = PATTERN % prefix
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                list_of_identifiers.append({source_id: match})

    return list_of_identifiers


def iter_rows(conn, dataset, table, orderby, bufsize=100, **filter):
    """Yield keyed rows from dataset table lazily and effective (using buffer).

    Args:
        conn (dict): connection dict
        dataset (str): dataset name (e.g. warehouse/database)
        table (str): table name
        order_by (str): how to order rows
        bufsize (int): how many rows to get per query
        filter (dict): additional field filter

    Yields:
        dict: the next row from table

    """
    offset = 0
    query = filter
    query['order_by'] = orderby
    while True:
        query['_offset'] = offset
        query['_limit'] = bufsize
        count = conn[dataset][table].find(return_count=True, **query)
        if not count:
            break
        rows = conn[dataset][table].find(**query)
        offset += bufsize
        for row in rows:
            # Fixing hex representation
            for field in ['id', 'meta_id']:
                if field in row:
                    try:
                        row[field] = uuid.UUID(row[field]).hex
                    except ValueError:
                        # Ignore errors if ID fields aren't UUIDs
                        pass
            yield row


def find_trial_by_identifiers(conn, identifiers, ignore_record_id=None):
    """Find first trial matched by one of passed identifiers.

    Args:
        conn (dict): connection dict
        identifiers (dict): identifiers dict (nct: <id>, euct: <id>, ...)
        ignore_record_id (str): skip record with this id (for better dedup)

    Returns:
        dict: trial

    """
    trial = None
    # See https://github.com/opentrials/processors/pull/46/files/f5e8403072bf6ed93b82d0c45bd3877e42e435c4#r76836368
    QUERY = "SELECT * FROM records WHERE identifiers @> '%s'"
    for source, identifier in identifiers.items():
        query = QUERY % json.dumps({source: identifier})
        records = list(conn['database'].query(query))
        for record in records:
            if (ignore_record_id and record['id'].hex == uuid.UUID(ignore_record_id).hex):
                continue
            trial = conn['database']['trials'].find_one(id=record['trial_id'].hex)
            if trial:
                break
        if trial:
            break
    return trial
