# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import re
import json
import uuid
import string
import logging
import datetime
import urlparse
import csv
import iso3166

from fuzzywuzzy import process, fuzz
from . import pybossa_tasks_updater
logger = logging.getLogger(__name__)
PyBossaTasksUpdater = pybossa_tasks_updater.PyBossaTasksUpdater


# Module API

EDIT_DISTANCE_THRESHOLD = 75


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


def clean_identifiers(identifiers):
    """Remove invalid identifiers.
    """
    PATTERNS = {
        'actrn': r'^ACTRN\d{14}p?$',
        'chictr': r'^ChiCTR',
        'drks': r'^DRKS',
        'euctr': r'^EUCTR\d{4}-\d{6}-\d{2}$',
        'gsk': r'^GSK',
        'irct': r'^IRCT',
        'isrctn': r'^ISRCTN\d{8}$',
        'jprn': r'^(JPRN-)?(C\d{9}|JapicCTI-\d{6}|JMA-IIA\d{5}|UMIN\d{9})$',
        'kct': r'^KCT',
        'nct': r'^NCT\d{8}$',
        'ntr': r'^NTR',
        'pactr': r'^PACTR',
        'per': r'^PER',
        'rbr': r'^RBR',
        'rpcec': r'^RPCEC',
        'takeda': r'^TAKEDA',
        'tctr': r'^TCTR',
        'who': r'^U\d{4}-\d{4}-\d{4}$',
    }
    result = {}
    for key, value in identifiers.items():
        try:
            new_value, num_changes = re.subn(
                r'^(\w+)\s+', r'\g<1>', value, re.IGNORECASE)
            if num_changes:
                logger.debug('Removed whitespaces from identifier "%s" to "%s"',
                             value, new_value)
                value = new_value
        except TypeError:
            pass
        if not validate_identifier(value):
            logger.warning('Ignoring invalid identifier %s:%s', key, value)
        elif key not in PATTERNS or not re.match(PATTERNS[key], value, re.IGNORECASE):
            message = 'Identifier "%s:%s" is not recognized'
            logger.warning(message, key, value)
        else:
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
    """Find list of valid trial identifier dicts in the given text.

    Example:
        [{'nct': 'NCT123345'}, {'euctr': 'EUCTR12345'}]

    It will only return identifiers that are valid according to
    validate_identifiers() function.
    """

    # Pattern could be improved based on a extended
    # clinical trial identifiers format analysis
    PATTERN = r'(%s\s*[\w\d-]{3,})'
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
                clean_ids = clean_identifiers({source_id: match})
                if clean_ids:
                    list_of_identifiers.extend([clean_ids])

    return list_of_identifiers


def validate_identifier(identifier):
    """Empty or identifiers with only zeros are invalid."""
    if identifier:
        numbers = re.sub('[^\d]', '', identifier)
        if numbers:
            return int(numbers) != 0


def validate_remote_url(url):
    """"URLs without domain and scheme or with a file scheme are invalid"""
    is_valid_url = False
    try:
        parsed_url = urlparse.urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            is_valid_url = (parsed_url.scheme != 'file')
    except AttributeError:
        pass

    return is_valid_url


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
            trial = conn['database']['trials'].find_one(
                id=record['trial_id'].hex)
            if trial:
                break
        if trial:
            break
    return trial


def safe_prepend(prepend_string, string):
    """Prepend to string non-destructively
    Ex: safe_prepend('EUCTR', 'EUCTR12345678') => 'EUCTR12345678'

    Args:
        prepend_string: string to prepend
        string: string to prepend to
    """
    if string is None:
        return None
    if not string.startswith(prepend_string):
        string = '%s%s' % (prepend_string, string)

    return string


def get_canonical_location_name(location):
    """Find the canonical location name according to the
    passed entry

    Args:
        location (str): the location to be normalized
    """

    # This auxiliar file is provided by the dataset repository of github.com and
    # can be checked on its latest version on the project website
    # See: https://github.com/datasets/country-codes/blob/master/data/country-codes.csv
    #
    # To create e new entry (or update an existing one), add a new line (or find the
    # existing one) and fill in the informations according to the header (line 1) order,
    # separating fields using comma
    CSV_PATH = 'data/countries.csv'
    ALPHA_3_HEADER = 'ISO3166-1-Alpha-3'
    DISTANCE_SCORER = fuzz.token_sort_ratio
    SCORE_INDEX = 1

    clean_string = lambda u: re.sub(u"[^\w\d'\s]+", '', u).lower()
    # Try to fetch canonical name directly from the iso-3166 country standard
    try:
        return iso3166.countries.get(clean_string(location)).name
    # If country isn't found on iso-3166 country list
    except KeyError:
        with open(os.path.join(os.path.dirname(__file__), CSV_PATH), 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            # Store information about the current match
            current_match = location
            current_score = float("-inf")
            for country in reader:
                # Extract relevant comparative info from the current country
                relevant_info = [unicode(country[field], encoding="utf-8")
                                 for field in reader.fieldnames[0:5]]
                # Do some string clean up and extract the most similar field (according
                # to Levenshtein scoring) over all the location relevant informations
                cleaned_location = clean_string(location)
                location_info = [location_info.lower() for location_info in relevant_info]
                choice = process.extractOne(cleaned_location, location_info, scorer=DISTANCE_SCORER)

                # Update current match if the distance score is above the current max score
                if choice[SCORE_INDEX] > current_score:
                    current_match = iso3166.countries.get(country[ALPHA_3_HEADER]).name
                    current_score = choice[SCORE_INDEX]

            if current_score < EDIT_DISTANCE_THRESHOLD:
                logger.debug('Location "%s" not normalized', location)
                return location

            return current_match
