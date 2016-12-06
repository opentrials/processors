# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import uuid

@pytest.fixture
def trial(conn, nct_source):
    trial = {
        'id': uuid.uuid1().hex,
        'identifiers': {'nct': 'NCT00212927'},
        'registration_date': '2005-09-13',
        'public_title': 'Continuity of Care and Outcomes After Discharge From Hospital',
        'brief_summary': None,
        'scientific_title': 'Patient Outcomes After Discharge From Hospital',
        'description': 'See above',
        'recruitment_status': 'not_recruiting',
        'eligibility_criteria': None,
        'first_enrollment_date': '2002-10-01',
        'study_type': 'Observational',
        'study_design': 'Prospective',
        'study_phase': None,
        'primary_outcomes': None,
        'secondary_outcomes': None,
        'has_published_results': False,
        'gender': 'both',
        'status': 'complete',
        'completion_date': '2006-10-13',
        'source_id': nct_source,
    }
    trial_id = conn['database']['trials'].insert(trial)
    return trial_id
