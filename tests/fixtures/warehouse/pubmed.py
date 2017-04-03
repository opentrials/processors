# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import pytest
import datetime

@pytest.fixture
def pubmed_record(conn):
    record =  {
        'meta_id': uuid.uuid1().hex,
        'meta_source': 'http://www.ncbi.nlm.nih.gov/pubmed/23571166',
        'meta_created': datetime.date(2016, 12, 11),
        'meta_updated': datetime.date(2016, 12, 11),
        'pmid': '23571166',
        'date_created': datetime.date(2013, 10, 9),
        'date_revised': datetime.date(2014, 8, 20),
        'country': 'United States',
        'medline_ta': 'Hum Vaccin Immunother',
        'nlm_unique_id': '101572652',
        'issn_linking': '2164-5515',
        'journal_issn': '2164-554X',
        'journal_title': 'Human vaccines & immunotherapeutics',
        'journal_iso': 'Hum Vaccin Immunother',
        'article_title': 'Article about healing',
        'article_abstract': 'How to heal people',
        'article_authors': ['Pierre Van Damme', 'Froukje Kafeja', 'Vinod Bambure'],
        'article_language': 'eng',
        'article_publication_type_list': None,
        'article_vernacular_title': None,
        'article_date': datetime.date(2013, 3, 23),
        'publication_status': 'publish',
        'article_ids': {
            'pii': '24504',
            'doi': '10.4161/hv.24504',
            'pubmed': '23571166',
        },
        'mesh_headings': None,
        'registry_ids': [
            {'ClinicalTrials.gov': 'NCT00968526'},
            {'ClinicalTrials.gov': 'NCT01001169'},
        ],
    }

    record_id = conn['warehouse']['pubmed'].insert(record)
    return record_id
