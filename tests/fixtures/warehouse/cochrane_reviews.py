# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import pytest

@pytest.fixture
def cochrane_review(conn):
    review = {
        'id': uuid.uuid1().hex,
        'study_type': 'MIX',
        'file_name': 'Sulpiride for schizophrenia [v9.0-For publication].rm5',
        'meta_source': 'http://datastore.opentrials.net/uploads/d7823d80-6f81-11e6-87af-931e370d0cf8/cochrane_schizophrenia_reviews.zip',
        'doi_id': '10.1002/14651858.CD001162',
        'study_id': 'STD-Soni-1990',
        'robs': [
            {
                'result': 'YES',
                'rob_id': 'QIT-02',
                'group_id': '',
                'modified': '',
                'rob_name': 'Allocation concealment?',
                'study_id': 'STD-Soni-1990',
                'group_name': '', 'rob_description':
                'Was allocation adequately concealed?',
                'result_description': 'A - Adequate',
            },
        ],
        'refs': [
            {
                'no': '',
                'pg': '233-8',
                'vl': '5', 'type':
                'JOURNAL_ARTICLE',
                'year': '1990',
                'title': 'Sulpiride in negative schizophrenia - a placebo-controlled double-blind assessment',
                'source': 'Human Psychopharmacology Clinical and Experimental',
                'authors': 'Soni SD, Mallik A, Schiff AA',
                'country': '',
                'identifiers': [],
            },
        ],
    }
    review_id = conn['warehouse']['cochrane_reviews'].insert(review)
    return review_id
