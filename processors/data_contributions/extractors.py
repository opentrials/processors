# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def extract_source():
    return {
        'id': 'contribution',
        'name': 'Data Contribution',
        'type': 'other',
    }


def extract_document(record):
    document = {
        'document_category_id': record['document_category_id'],
        'source_url': record['data_url'] or record['url'],
    }
    if record['document_id']:
        document['id'] = record['document_id']
    return document
