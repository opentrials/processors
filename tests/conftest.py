# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
import dataset
import betamax
import os
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
import processors.base.config as config

# Make fixtures available to all tests

from tests.fixtures.api.files import file_fixture, fda_file
from tests.fixtures.api.trials import trial
from tests.fixtures.api.sources import nct_source, fda_source, euctr_source
from tests.fixtures.api.fda_approvals import fda_approval
from tests.fixtures.api.fda_applications import fda_application
from tests.fixtures.api.organizations import organization
from tests.fixtures.api.records import record
from tests.fixtures.api.documents import fda_document
from tests.fixtures.api.documents import document
from tests.fixtures.api.document_categories import document_category

from tests.fixtures.warehouse.cochrane_reviews import cochrane_review
from tests.fixtures.warehouse.nct import nct_record
from tests.fixtures.warehouse.pubmed import pubmed_record

from tests.fixtures.explorer.data_contributions import data_contribution

# Betamax config

with betamax.Betamax.configure() as cfg:
    cfg.cassette_library_dir = 'tests/cassettes/'

    record_mode = 'none' if os.environ.get('CI') else 'once'
    cfg.default_cassette_options['record_mode'] = record_mode
    cfg.default_cassette_options['match_requests_on'] = [
        'uri',
        'headers',
        'body',
    ]

@pytest.fixture
def conn(request):
    """Create connection dict for the test databases.
        New sessions are created for each test and are closed at the end of the test.

    Returns:
        a connection dict where each key is a database name and each value
         a `dataset.Database()` instance
    """

    conn = {
        'database': dataset.connect(config.DATABASE_URL),
        'warehouse': dataset.connect(config.WAREHOUSE_URL),
        'explorer': dataset.connect(config.EXPLORER_URL),
    }

    APISession = sessionmaker(bind=conn['database'].engine)
    api_session = APISession()
    WarehouseSession = sessionmaker(bind=conn['warehouse'].engine)
    warehouse_session = WarehouseSession()
    ExplorerSession = sessionmaker(bind=conn['explorer'].engine)
    explorer_session = ExplorerSession()
    def teardown():
        truncate_database(conn['database'].engine)
        truncate_database(conn['warehouse'].engine)
        truncate_database(conn['explorer'].engine)
        api_session.close()
        warehouse_session.close()
        explorer_session.close()

    request.addfinalizer(teardown)
    return conn


def truncate_database(engine):
    metadata = MetaData(bind=engine)
    metadata.reflect()

    connection = engine.connect()
    transaction = connection.begin()
    for table in reversed(metadata.sorted_tables):
        connection.execute(table.delete())
    transaction.commit()
