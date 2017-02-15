# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


def write_document_category(conn, document_category):
    """Write document category to database.

    Args:
        conn (dict): connection dict
        document category (dict): document category data

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str: object identifier

    """
    create = False
    db = conn['database']

    # This is used to sinchronize with `data_categories` of `data_contributions`
    if document_category.get('id'):
        obj = db['document_categories'].find_one(id=document_category['id'])
        if not obj:
            obj = {
                'id': document_category['id'],
            }
            create = True

    # This document category is not specific to data contributions
    else:
        obj = db['document_categories'].find_one(name=document_category['name'],
            group=document_category['group'])
        if not obj:
            # Avoid ids that could be overwritten by syncronization with `data_categories`
            max_id_query = 'SELECT max(id) FROM document_categories;'
            max_id_result = [res['max'] for res in db.query(max_id_query)]
            max_id = max_id_result[0] or 0
            obj = {
                'id': (max_id % 100) + 101,
            }
            create = True

    # Update object
    obj.update({
        'name': document_category['name'],
        'group': document_category['group'],
    })

    # Write object
    db['document_categories'].upsert(obj, ['id'], ensure=False)

    logger.debug('Document category %s-%s: %s', document_category['group'],
                document_category['name'], 'created' if create else 'updated')
    return obj['id']
