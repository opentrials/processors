# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def extract_review_results(review_results):
    """Extract results from reference"""

    correlations = {'sequence generation': 'sequence generation',
                    'allocation concealment': 'allocation concealment',
                    'blinding (performance and/or detection)': 'blinding',
                    'blinding (performance)': 'performance bias',
                    'blinding (detection)': 'detection bias',
                    'attrition': 'incomplete outcome',
                    'reporting': 'selective reporting',
                    'other biases': 'other bias'}
    results = []

    for result in review_results:
        name = None
        rob_name = result.get('rob_name') or ''
        matches = {name: val for name, val in correlations.items()
                   if val in rob_name.lower()}
        matched_values = sorted(list(matches.values()))
        if len(matched_values) > 1:
            if matched_values == ['blinding', 'performance bias']:
                name = 'blinding (performance)'
            elif matched_values == ['blinding', 'detection bias']:
                name = 'blinding (detection)'
            elif matched_values == ['blinding', 'detection bias',
                                    'performance bias']:
                name = 'blinding (performance and/or detection)'

        elif len(matched_values) == 1:
            name = matches.keys()[0]

        if name:
            results.append({'name': name, 'value': result['result'].lower()})

    return results


def extract_source(record):
    return {
        'id': 'cochrane_schizophrenia',
        'name': 'Cochrane Schizophrenia Group',
        'type': 'other',
        'source_url': 'http://schizophrenia.cochrane.org/',
    }


def extract_rob(record, trial_id, source_id):
    doi_id = record['doi_id']
    source_url = 'http://onlinelibrary.wiley.com/doi/{0}/full'.format(doi_id)
    return {
        'trial_id': str(trial_id),
        'source_url': source_url,
        'study_id': record['study_id'],
        'source_id': source_id
    }


def extract_rob_rob_criteria(record, rob_id, rob_criteria_id):
    return {
        'risk_of_bias_id': rob_id,
        'risk_of_bias_criteria_id': rob_criteria_id,
        'value': record['value']
    }


def extract_rob_criteria(record):
    return {'name': record['name']}
