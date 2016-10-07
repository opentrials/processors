# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
from .. import writers
logger = logging.getLogger(__name__)


# Module API

def process_risk_of_biases(conn, extractors, review, trial_id):
    """Translate risk_of_bias records from warehouse to database.

    Args:
        conn (dict): connection dict
        extractors (dict): extractors dict
        review (dict): review that has been matched with a trial
        trial_id (string): trial id that has been matched with a review
    """

    # Extract and write source
    source = extractors['extract_source'](None)
    source_id = writers.write_source(conn, source)

    errors = 0
    success = 0

    conn['database'].begin()

    try:

        # Extract and write risk_of_bias, risk_of_bias_criteria
        # and risk_of_bias-risk_of_bias_criteria
        rob = extractors['extract_rob'](review, trial_id, source_id)
        rob_id = writers.risk_of_bias.write_rob(conn, rob)

        review_results = extractors['extract_review_results'](review['robs'])
        for result in review_results:
            rob_crt = extractors['extract_rob_criteria'](result)
            rob_crt_id = writers.risk_of_bias.write_rob_criteria(conn, rob_crt)

            rob_rob_crt = extractors['extract_rob_rob_criteria'](result, rob_id,
                                                                 rob_crt_id)
            writers.risk_of_bias.write_rob_rob_criteria(conn, rob_rob_crt)

    except Exception as exception:
        errors += 1
        conn['database'].rollback()
        logger.exception('Processing error: %s [%s]',
            repr(exception), errors)

    else:
        success += 1
        conn['database'].commit()
        if not success % 100:
            logger.info('Processed %s cohrane reviews from %s', success)
