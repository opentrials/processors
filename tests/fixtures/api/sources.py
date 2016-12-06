# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest


@pytest.fixture
def nct_source(conn):
    source = {
        'id': 'nct',
        'name': 'ClinicalTrials.gov',
        'type': 'register',
        'source_url': 'https://clinicaltrials.gov',
        'terms_and_conditions_url': 'https://clinicaltrials.gov/ct2/about-site/terms-conditions',
    }
    source_id = conn['database']['sources'].insert(source)
    return source_id


@pytest.fixture
def fda_source(conn):
    source = {
        'id': 'fda',
        'name': 'U.S. Food and Drug Administration',
        'type': 'other',
        'source_url': 'http://www.fda.gov',
    }
    source_id = conn['database']['sources'].insert(source)
    return source_id


@pytest.fixture
def euctr_source(conn):
    source = {
        'id': 'euctr',
        'name': 'EU Clinical Trials Register',
        'type': 'register',
        'source_url': 'https://www.clinicaltrialsregister.eu',
        'terms_and_conditions_url': 'https://www.clinicaltrialsregister.eu/disclaimer.html',
      }
    source_id = conn['database']['sources'].insert(source)
    return source_id
