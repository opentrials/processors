# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import logging
import datetime
from . import write_organisation
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_fda_application(conn, fda_application, source_id):
    """Write fda_application to database.

    Args:
        conn (dict): connection dict
        fda_application (dict): normalized data
        source_id (str): data source id

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    timestamp = datetime.datetime.utcnow()

    if 'organisation' in fda_application:
        organisation_name = fda_application['organisation']
        del fda_application['organisation']
        slug = helpers.slugify_string(organisation_name)
        organisation = conn['database']['organisations'].find_one(slug=slug)
        if not organisation:
            organisation = {
                'name': organisation_name,
                'slug': slug,
            }
            organisation_id = write_organisation(conn, organisation, source_id)
        else:
            organisation_id = organisation['id']
        fda_application['organisation_id'] = organisation_id

    fda_application['updated_at'] = timestamp
    conn['database']['fda_applications'].upsert(fda_application,
                                                ['id'],
                                                ensure=False)
    # Log debug
    logger.debug('FDA Application upserted: %s', fda_application['id'])

    return fda_application['id']
