# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from processors.base import helpers
import processors.cochrane_reviews.extractors as extractors_module
from processors.base.processors.risk_of_bias import process_risk_of_biases


class TestRiskOfBiasProcessor(object):
    def test_creates_risk_of_bias_if_for_publication(self, conn, extractors,
        cochrane_review, trial):

        review_attrs = {
            'id': cochrane_review,
            'file_name': 'For publication',
        }
        conn['warehouse']['cochrane_reviews'].update(review_attrs, ['id'])
        updated_review = conn['warehouse']['cochrane_reviews'].find_one(id=cochrane_review)

        process_risk_of_biases(conn, extractors, updated_review, trial)
        created_robs = [rob for rob in conn['database']['risk_of_biases'].all()]

        assert len(created_robs) == 1


    def test_doesnt_create_risk_of_bias_if_not_for_publication(self, conn,
        extractors, cochrane_review, trial):

        review_attrs = {
            'id': cochrane_review,
            'file_name': 'No publication for this one',
        }
        conn['warehouse']['cochrane_reviews'].update(review_attrs, ['id'])
        updated_review = conn['warehouse']['cochrane_reviews'].find_one(id=cochrane_review)

        process_risk_of_biases(conn, extractors, updated_review, trial)
        created_robs = [rob for rob in conn['database']['risk_of_biases'].all()]

        assert len(created_robs) == 0


    def test_creates_risk_of_bias_criteria(self, conn, cochrane_review,
        extractors, rob, trial):

        review_attrs = {
            'id': cochrane_review,
            'file_name': 'For publication',
            'robs': [rob],
        }
        conn['warehouse']['cochrane_reviews'].update(review_attrs, ['id'])
        updated_review = conn['warehouse']['cochrane_reviews'].find_one(id=cochrane_review)

        process_risk_of_biases(conn, extractors, updated_review, trial)
        rob_criterias = [rc for rc in conn['database']['risk_of_bias_criterias'].all()]

        assert len(rob_criterias) == 1


    def test_creates_risk_of_bias_and_risk_of_bias_criteria(self, conn, cochrane_review,
        extractors, rob, trial):

        review_attrs = {
            'id': cochrane_review,
            'file_name': 'For publication',
            'robs': [rob],
        }
        conn['warehouse']['cochrane_reviews'].update(review_attrs, ['id'])
        updated_review = conn['warehouse']['cochrane_reviews'].find_one(id=cochrane_review)

        process_risk_of_biases(conn, extractors, updated_review, trial)
        rob_rob_criterias = [rc for rc in conn['database']['risk_of_biases_risk_of_bias_criterias'].all()]

        assert len(rob_rob_criterias) == 1
        assert rob_rob_criterias[0]['value'] == 'yes'


@pytest.fixture
def extractors():
    return helpers.get_variables(extractors_module,
        lambda x: x.startswith('extract_'))

@pytest.fixture
def rob():
    return {
        'result': 'YES',
        'rob_id': 'QIT-02',
        'rob_name': 'Allocation concealment',
        'result_description': 'A - Adequate',
    }
