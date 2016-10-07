# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime
logger = logging.getLogger(__name__)


def write_rob(conn, rob):
    """Write risk_of_bias to database.

    Args:
        conn (dict): connection dict
        rob (dict): risk_of_bias data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Search for existing risk of bias
    ex_rob = conn['database']['risk_of_biases'].find_one(study_id=rob['study_id'],
                                                         source_url=rob['source_url'])

    # Create object
    if not ex_rob:
        ex_rob = {
            'id': uuid.uuid1().hex,
            'created_at': timestamp,
            'source_url': rob['source_url'],
            'study_id': rob['study_id'],
        }
        create = True

    # Update object
    if ex_rob.get('trial_id') != rob.get('trial_id') or \
       ex_rob.get('source_id') != rob.get('source_id'):
        ex_rob.update({
            'updated_at': timestamp,
            # ---
            'trial_id': rob['trial_id'],
            'source_id': rob['source_id'],
        })

        # Write object
        conn['database']['risk_of_biases'].upsert(ex_rob, ['id'], ensure=False)

        # Log debug
        logger.debug('Risk of bias - %s: %s',
                     'created' if create else 'updated', ex_rob['source_url'])

    return ex_rob['id']


def write_rob_criteria(conn, rob_criteria):
    """Write risk_of_bias_criteria to database.

    Args:
        conn (dict): connection dict
        rob_criteria (dict): risk_of_bias_criteria data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

   """
    timestamp = datetime.datetime.utcnow()

    # Search for existing risk of bias criteria
    rob_criteria_db = conn['database']['risk_of_bias_criterias']
    ex_rob_crt = rob_criteria_db.find_one(name=rob_criteria['name'])

    # Create object
    if not ex_rob_crt:
        ex_rob_crt = {
            'id': uuid.uuid1().hex,
            'created_at': timestamp,
            'updated_at': timestamp,
            'name': rob_criteria['name'],
        }

        # Write object
        conn['database']['risk_of_bias_criterias'].upsert(ex_rob_crt, ['id'],
                                                          ensure=False)

        # Log debug
        logger.debug('Risk of bias criteria - created: %s', ex_rob_crt['name'])

    return ex_rob_crt['id']


def write_rob_rob_criteria(conn, rob_rob_criteria):
    """Write risk_of_bias-risk_of_bias_criteria to database.

    Args:
        conn (dict): connection dict
        rob_rob_criteria (dict): risk_of_bias risk_of_bias_criteria data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        None

   """

    # Write object
    db = conn['database']['risk_of_biases_risk_of_bias_criterias']
    db.upsert(rob_rob_criteria, keys=['risk_of_bias_id', 'risk_of_bias_criteria_id'],
              ensure=False)

    return None
