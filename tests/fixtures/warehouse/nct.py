# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import pytest
import datetime

@pytest.fixture
def nct_record(conn):
    record =  {
        'meta_id': uuid.uuid1().hex,
        'meta_source': 'https://clinicaltrials.gov/ct2/show/results/NCT12345678',
        'meta_created': datetime.date(2016, 12, 11),
        'meta_updated': datetime.date(2016, 12, 11),
        'nct_id': 'NCT12345678',
        'brief_title': 'Public title',
        'official_title': 'Scientific title',
        'clinical_results': False,
        'firstreceived_date': datetime.date(2016, 1, 1),
        'brief_summary': 'Brief summary',
        'detailed_description': 'Detailed description',
        'eligibility': None,
        'start_date': datetime.date(2016, 1, 1),
        'study_type': 'Study type',
        'study_design': 'Study design',
        'phase': 'Phase',
        'primary_outcomes': 'Primary outcomes',
        'secondary_outcomes': 'Secondary outcomes',
        'secondary_ids': ['ISRCTN71203361'],
        'completion_date_actual': datetime.date(2016, 12, 12),
        'results_exemption_date': datetime.date(2016, 11, 9),
    }

    record_id = conn['warehouse']['nct'].insert(record)
    return record_id
