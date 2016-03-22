# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import dataset
import sqlalchemy as sa
from sqlalchemy.dialects.postgres import ARRAY

from . import settings
from .mapper import Mapper


# Module API

def cli():

    logging.basicConfig(level=logging.INFO)

    warehouse = dataset.connect(settings.WAREHOUSE_URL)
    database = dataset.connect(settings.DATABASE_URL)

    # Create columns
    # TODO: move to api migrations
    for table in ['interventions', 'locations', 'organisations', 'persons', 'problems', 'records', 'sources', 'trials']:
        if 'created' not in database[table]:
            database[table].create_column('created', sa.DateTime(timezone=True))
        if 'updated' not in database[table]:
            database[table].create_column('updated', sa.DateTime(timezone=True))
        if 'links' not in database[table]:
            database[table].create_column('links', ARRAY(sa.Text))
            database.query('CREATE INDEX %s_links_idx on %s USING GIN(links)' % (table, table))
        if 'facts' not in database[table]:
            database[table].create_column('facts', ARRAY(sa.Text))
            database.query('CREATE INDEX %s_facts_idx on %s USING GIN(facts)' % (table, table))

    mapper = Mapper(warehouse, database)
    mapper.map(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    cli()
